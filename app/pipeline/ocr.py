import cv2
import pytesseract

def expand_bbox(bbox, img_shape, pad=8):
    x1, y1, x2, y2 = bbox
    h, w = img_shape[:2]

    return (
        max(0, x1 - pad),
        max(0, y1 - pad),
        min(w, x2 + pad),
        min(h, y2 + pad),
    )

def recognize_text(image, bboxes):
    texts = []

    for bbox in bboxes:
        x1, y1, x2, y2 = expand_bbox(bbox, image.shape, pad=8)
        crop = image[y1:y2, x1:x2]

        crop = cv2.resize(crop, None, fx=2, fy=2, interpolation=cv2.INTER_CUBIC)
        gray = cv2.cvtColor(crop, cv2.COLOR_BGR2GRAY)
        gray = cv2.threshold(
            gray, 0, 255,
            cv2.THRESH_BINARY + cv2.THRESH_OTSU
        )[1]

        config = "--psm 6 -l rus+eng"

        text = pytesseract.image_to_string(gray, config=config)
        text = text.strip().replace("\n", " ")
        texts.append(text.strip())

    return texts
