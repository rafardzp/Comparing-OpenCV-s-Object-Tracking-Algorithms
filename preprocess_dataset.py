import cv2
import os
import shutil

def create_video_from_images(image_folder, video_name):
    images = [img for img in os.listdir(image_folder) if img.endswith(".jpg")]
    frame = cv2.imread(os.path.join(image_folder, images[0]))
    height, width, layers = frame.shape

    video = cv2.VideoWriter(video_name, 0, 30, (width, height))

    for image in images:
        video.write(cv2.imread(os.path.join(image_folder, image)))

    cv2.destroyAllWindows()
    video.release()

if __name__ == '__main__':
    folders = [folder for folder in os.listdir("Videos/val") if 
               os.path.isdir(os.path.join("Videos/val", folder)) and "GT" not in folder]

    for i, folder in enumerate(folders):
        # Create video
        create_video_from_images(os.path.join("Videos/val", folder), f"Videos/video00{i}" + ".avi")

        # Extract GT
        gt_file_path = os.path.join("Videos/val", folder, "groundtruth.txt")
        if os.path.exists(gt_file_path):
            new_gt_file_path = os.path.join("Videos/GT", f"video00{i}.txt")
            shutil.move(gt_file_path, new_gt_file_path)