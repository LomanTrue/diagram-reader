from app.pipeline.preprocess import preprocess
from app.pipeline.detect import DiagramDetector
from app.pipeline.ocr import recognize_text
from app.graph.builder import build_graph
from app.describe.algorithm import describe_algorithm
from dataclasses import asdict

detector = DiagramDetector("models/detector.pt")

def process_image(image_bytes: bytes):
    image_rgb, image_gray = preprocess(image_bytes)
    detections = detector.detect(image_rgb)

    text_boxes = [d["bbox"] for d in detections if d["class"] == 1]
    texts = recognize_text(image_rgb, text_boxes)

    ocr_results = [{"bbox": bbox, "text": text} for bbox, text in zip(text_boxes, texts)]

    graph = build_graph(detections, ocr_results)
    description = describe_algorithm(graph)

    return {
        "graph": asdict(graph),
        "description": description
    }
