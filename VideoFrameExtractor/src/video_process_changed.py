import cv2
import os
import glob
import numpy as np

def save_frame_if_changed(prev_frame, current_frame, frame_number, output_folder, threshold=30):
    if prev_frame is None:
        return False

    # 프레임 간의 차이 계산
    diff = cv2.absdiff(current_frame, prev_frame)
    gray = cv2.cvtColor(diff, cv2.COLOR_BGR2GRAY)
    _, thresh = cv2.threshold(gray, threshold, 255, cv2.THRESH_BINARY)

    # 변화가 있는지 확인
    change = np.sum(thresh) > 0

    if change:
        cv2.imwrite(os.path.join(output_folder, f"frame_{frame_number:05d}.jpg"), current_frame)

    return change

def video_to_frames(video_path, output_folder, threshold=30):
    cap = cv2.VideoCapture(video_path)
    frame_number = 0
    prev_frame = None

    try:
        if not os.path.exists(output_folder):
            os.makedirs(output_folder)

        while True:
            ret, frame = cap.read()
            if not ret:
                break

            if save_frame_if_changed(prev_frame, frame, frame_number, output_folder, threshold):
                frame_number += 1
            prev_frame = frame.copy()
    finally:
        cap.release()

def process_videos_in_directory(directory, threshold=30):
    for video_file in glob.glob(os.path.join(directory, '*.mp4')):
        print(f"Processing: {video_file}")
        output_folder = os.path.splitext(video_file)[0] + '_changed_frames'
        video_to_frames(video_file, output_folder, threshold)

# videos 폴더 내의 모든 MP4 파일을 처리
process_videos_in_directory('../video')