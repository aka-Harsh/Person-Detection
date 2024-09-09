import cv2
import numpy as np
from src.person_detector import PersonDetector
from src.person_tracker import PersonTracker

class VideoProcessor:
    def __init__(self, model_name="yolov8n.pt", conf_threshold=0.5):
        self.detector = PersonDetector(model_name, conf_threshold)
        self.tracker = PersonTracker(max_disappeared=30, max_distance=100)

    def process_video(self, input_path, output_path):
        cap = cv2.VideoCapture(input_path)
        width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        fps = int(cap.get(cv2.CAP_PROP_FPS))

        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        out = cv2.VideoWriter(output_path, fourcc, fps, (width, height))

        frame_count = 0
        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                break

            frame_count += 1
            detections = self.detector.detect(frame)
            rects = [d['bbox'] for d in detections]
            objects = self.tracker.update(rects)

            for (objectID, centroid) in objects.items():
                text = f"ID {objectID}"
                cv2.putText(frame, text, (centroid[0] - 10, centroid[1] - 10),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
                cv2.circle(frame, (centroid[0], centroid[1]), 4, (0, 255, 0), -1)

            for detection in detections:
                bbox = detection['bbox']
                cv2.rectangle(frame, (bbox[0], bbox[1]), (bbox[2], bbox[3]), (255, 0, 0), 2)

            out.write(frame)

        cap.release()
        out.release()

    def process_all_videos(self, input_folder, output_folder):
        import os
        for filename in os.listdir(input_folder):
            if filename.endswith((".mp4", ".avi", ".mov")):
                input_path = os.path.join(input_folder, filename)
                output_path = os.path.join(output_folder, f"processed_{filename}")
                print(f"Processing {filename}...")
                self.process_video(input_path, output_path)
                print(f"Finished processing {filename}")