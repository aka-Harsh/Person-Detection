from ultralytics import YOLO
import os

class PersonDetector:
    def __init__(self, model_name="yolov8n.pt", conf_threshold=0.5):
        self.model_name = model_name
        self.conf_threshold = conf_threshold
        self.model_path = os.path.join("models", "weights", self.model_name)
        
        if not os.path.exists(self.model_path):
            print(f"Downloading {self.model_name}...")
            self.model = YOLO(self.model_name)
            self.model.save(self.model_path)
        else:
            self.model = YOLO(self.model_path)
        
    def detect(self, frame):
        results = self.model(frame)
        
        detections = []
        for r in results:
            boxes = r.boxes
            for box in boxes:
                x1, y1, x2, y2 = box.xyxy[0]
                conf = box.conf[0]
                cls = box.cls[0]
                
                if int(cls) == 0 and conf > self.conf_threshold:  # 0 is the class index for 'person'
                    detections.append({
                        'bbox': [int(x1), int(y1), int(x2), int(y2)],
                        'conf': float(conf),
                        'class': 'person'
                    })
        
        return detections