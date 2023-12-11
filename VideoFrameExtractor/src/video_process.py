import cv2
import os
import glob

def video_to_frames(video_path, output_folder):
    cap = cv2.VideoCapture(video_path)
    frame_number = 0

    try:
        if not os.path.exists(output_folder):
            os.makedirs(output_folder)

        while True:
            ret, frame = cap.read()
            if not ret:
                break

            frame_file = os.path.join(output_folder, f"frame_{frame_number:05d}.jpg")
            cv2.imwrite(frame_file, frame)
            frame_number += 1
    finally:
        cap.release()

def process_videos_in_directory(directory):
    for video_file in glob.glob(os.path.join(directory, '*.mp4')):
        print(f"Processing: {video_file}")
        output_folder = os.path.splitext(video_file)[0]
        video_to_frames(video_file, output_folder)

# videos 폴더 내의 모든 MP4 파일을 처리
process_videos_in_directory('../videos')