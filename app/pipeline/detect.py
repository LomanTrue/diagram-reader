from ultralytics import YOLO
from typing import List, Dict

class DiagramDetector:
    def __init__(self, model_path: str):
        self.model = YOLO(model_path)

    def detect(self, image) -> List[Dict]:
        results = self.model(image)
        detections = []

        for r in results:
            for box, conf, cls in zip(r.boxes.xyxy, r.boxes.conf, r.boxes.cls):
                detections.append({
                    "bbox": [int(x) for x in box],
                    "score": float(conf),
                    "class": int(cls)
                })
        return detections
