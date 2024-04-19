import cv2
import numpy as np
import scipy.io
import argparse
import sys
import csv
import os

# Function to parse arguments from terminal
def parse_args():
    ap = argparse.ArgumentParser(description="Evaluate a specified tracker on a video set and extract performance metrics")
    ap.add_argument("-t", "--tracker", type=str, help="String defining the tracker")
    ap.add_argument("-s", "--store_videos", action='store_false', 
                    help="Boolean to define if videos are saved", default=True)
    ap.add_argument("-v", "--verbose", action='store_false', 
                    help="Boolean to define if videos are shown", default=True)
    
    if len(sys.argv) == 1:
        ap.print_help()
        sys.exit(1)

    args = ap.parse_args()
    return args

# Function to select the tracker based on its name
def create_tracker(tracker_type):
    if tracker_type == 'KCF':
        return cv2.legacy.TrackerKCF.create()
    
    elif tracker_type == 'CSRT':
        return cv2.legacy.TrackerCSRT.create()
    
    elif tracker_type == 'BOOSTING':
        return cv2.legacy.TrackerBoosting.create()
    
    elif tracker_type == 'MedianFlow':
        return cv2.legacy.TrackerMedianFlow.create()
    
    elif tracker_type == 'MIL':
        return cv2.legacy.TrackerMIL.create()
    
    elif tracker_type == 'MOSSE':
        return cv2.legacy.TrackerMOSSE.create()
    
    elif tracker_type == 'TLD':
        return cv2.legacy.TrackerTLD.create()
    
    elif tracker_type == 'GOTURN':
        params = cv2.TrackerGOTURN_Params()
        params.modelBin = "Models/goturn.caffemodel"
        params.modelTxt = "Models/goturn.prototxt"
        return cv2.TrackerGOTURN.create(params)
    
    elif tracker_type == 'DaSiamRPN':
        params = cv2.TrackerDaSiamRPN_Params()
        params.kernel_cls1 = "Models/dasiamrpn_kernel_cls1.onnx"
        params.kernel_r1 = "Models/dasiamrpn_kernel_r1.onnx"
        params.model = "Models/dasiamrpn_model.onnx"
        return cv2.TrackerDaSiamRPN.create(params)
    
    elif tracker_type == 'Nano':
        params = cv2.TrackerNano_Params()
        params.backbone = 'Models/nanotrack_backbone_sim.onnx'
        params.neckhead = 'Models/nanotrack_head_sim.onnx'
        return cv2.TrackerNano.create(params)
    
    elif tracker_type == 'Vit':
        params = cv2.TrackerVit_Params()
        params.net = "Models\object_tracking_vittrack_2023sep.onnx"
        return cv2.TrackerVit.create(params)
    
    else:
        return None

# Function to calculate IoU
def calculate_iou(bbox1, bbox2):
    x1, y1, w1, h1 = bbox1
    x2, y2, w2, h2 = bbox2

    # Get coordinates of intersection rectangle
    x_intersection = max(x1, x2)
    y_intersection = max(y1, y2)
    x_intersection_right = min(x1 + w1, x2 + w2)
    y_intersection_bottom = min(y1 + h1, y2 + h2)

    # Calculate area of intersection rectangle
    intersection_area = max(0, x_intersection_right - x_intersection + 1) * max(0, y_intersection_bottom - y_intersection + 1)

    # Calculate area of both bounding boxes
    bbox1_area = w1 * h1
    bbox2_area = w2 * h2

    # Calculate IoU
    iou = intersection_area / float(bbox1_area + bbox2_area - intersection_area)
    return iou

if __name__ == '__main__':

    # Parse arguments
    args = parse_args()
    print(f"Calling with args: {args}")

    # List of trackers to compare
    tracker_types = ['KCF', 'CSRT', 'BOOSTING', 'MedianFlow', 'MIL', 'MOSSE', 'TLD', 
                     'GOTURN', 'DaSiamRPN', 'Nano', 'Vit']
    
    if args.tracker not in tracker_types:
        print(f"The specified tracker is not available, please, define one of the following: ")
        print(tracker_types)
        sys.exit(1)

    # Path to the folders
    videos_folder = 'Videos/'
    gt_folder = 'Videos/GT/'
    output_folder = 'Output/'

    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    if args.store_videos and not os.path.exists(output_folder + "Videos/"):
        os.makedirs(output_folder + "Videos/")
    
    # Variable to store results
    results = []

    # Loop through each video in the folder
    for video_file in os.listdir(videos_folder):

        video_path = os.path.join(videos_folder, video_file)

        if os.path.isdir(video_path):
            continue

        video_name = os.path.splitext(video_file)[0]
        gt_file = os.path.join(gt_folder, f"{video_name}.txt")
        # gt_file = os.path.join(gt_folder, f"{video_name}.mat")

        # Read video
        video_capture = cv2.VideoCapture(video_path)

        # Read GT file
        with open(gt_file, 'r') as f:
            lines = f.readlines()
            gt_bbox_list = [[int(float(elem)) for elem in line.strip().split(',')] for line in lines]

        # gt_data = scipy.io.loadmat(gt_file)
        # gt_bbox_list = gt_data['labels']
        
        # Create video to save if needed
        frame_width = int(video_capture.get(cv2.CAP_PROP_FRAME_WIDTH))
        frame_height = int(video_capture.get(cv2.CAP_PROP_FRAME_HEIGHT))

        if args.store_videos:
            video_fps = video_capture.get(cv2.CAP_PROP_FPS)

            output_video_path = os.path.join(output_folder + 'Videos/', f'{video_name}_{args.tracker}_output.avi')
            fourcc = cv2.VideoWriter_fourcc(*'XVID')
            output_video = cv2.VideoWriter(output_video_path, fourcc, video_fps, (frame_width, frame_height))
        
        # Set fixed window size mantaining aspect ratio
        if args.verbose:
            max_window_width = 800
            max_window_height = 600

            aspect_ratio = frame_width / frame_height

            window_width = min(max_window_width, int(max_window_height * aspect_ratio))
            window_height = min(max_window_height, int(max_window_width / aspect_ratio))

            cv2.namedWindow(video_name, cv2.WINDOW_NORMAL)
            cv2.resizeWindow(video_name, window_width, window_height)

        # Read first frame
        success, frame = video_capture.read()
        if not success:
            continue

        # Initialize variables to store tracking results
        tracked_frames = 0
        total_time = 0
        fps = []
        iou = []
        total_failures = 0

        # Create tracker
        tracker = create_tracker(args.tracker)

        # Define object to track with first frame's ground truth
        gt_bbox = gt_bbox_list[tracked_frames]
        tracker.init(frame, gt_bbox)

        # Loop through the frames
        while True:
            # Read a new frame
            success, frame = video_capture.read()
            if not success:
                break

            # Start timer
            timer = cv2.getTickCount()

            # Update tracker
            success, bbox = tracker.update(frame)

            # Calculate Frames per Second (FPS)
            fps.append(cv2.getTickFrequency() / (cv2.getTickCount() - timer))

            # Calculate IoU and annotate video
            tracked_frames += 1

            if success:
                gt_bbox = gt_bbox_list[tracked_frames]
                iou.append(calculate_iou(gt_bbox, bbox))

                cv2.rectangle(frame, (int(gt_bbox[0]), int(gt_bbox[1])), (int(gt_bbox[0] + gt_bbox[2]), 
                                int(gt_bbox[1] + gt_bbox[3])), (0, 255, 0), 2)
                cv2.rectangle(frame, (int(bbox[0]), int(bbox[1])), (int(bbox[0] + bbox[2]), 
                                int(bbox[1] + bbox[3])), (0, 0, 255), 2)
                cv2.putText(frame, "FPS : " + str(int(fps[-1])), (20, 40), cv2.FONT_HERSHEY_DUPLEX, 0.75, (0, 0, 255), 2)

                if args.store_videos:
                    output_video.write(frame)

            else:
                total_failures += 1
                iou.append(0)
                cv2.putText(frame, "Tracking failure detected", (20, 40), cv2.FONT_HERSHEY_DUPLEX, 0.75, (0, 0, 255), 2)
                
                if args.store_videos:
                    output_video.write(frame)

            if args.verbose:
                cv2.imshow(video_name, frame)
                if cv2.waitKey(1) & 0xFF == 27:
                    break

        # Calculate average IoU and fps
        avg_iou = np.mean(iou)
        std_iou = np.std(iou)

        avg_fps = np.mean(fps)
        std_fps = np.std(fps)

        # Print results
        if args.verbose: 
            print(f"{args.tracker} tracker - Video: {video_name} - Average IoU: {avg_iou} - Average FPS: {avg_fps} - Failures: {total_failures}")

        results.append([args.tracker, video_name, avg_iou, std_iou, avg_fps, std_fps, total_failures])

        # Release video capture and close all windows
        video_capture.release()
        if args.store_videos:
            output_video.release()
        cv2.destroyAllWindows()

    # Write results to CSV file
    csv_file = os.path.join(output_folder, f'tracking_results_{args.tracker}.csv')

    with open(csv_file, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['Tracker', 'Video', 'Average IoU', 'STD IoU', 'Average FPS', 'STD FPS', 'N Failures'])
        writer.writerows(results)

    print(f"Results saved to {csv_file}")