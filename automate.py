import subprocess

if __name__ == '__main__':
    script_path = 'evaluate_tracker.py'
    trackers = ['KCF', 'CSRT', 'BOOSTING', 'MedianFlow', 'MIL', 'MOSSE', 'TLD', 'GOTURN', 
                'DaSiamRPN', 'Nano', 'Vit']

    for tracker in trackers:
        try:
            subprocess.run(f'python {script_path} --tracker {tracker} --store_videos')
        except Exception as e:
            print(f"Error evaluating tracker {tracker}: {e}")
            continue