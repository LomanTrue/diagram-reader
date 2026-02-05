from paddleocr import PaddleOCR

ocr = PaddleOCR(lang="en")

def recognize_text(image, bboxes):
    texts = []

    for bbox in bboxes:
        x1, y1, x2, y2 = bbox
        crop = image[y1:y2, x1:x2]
        result = ocr.ocr(crop)

        if result:
            text = " ".join([line[1][0] for line in result[0]])
            texts.append(text)
        else:
            texts.append("")

    return texts
