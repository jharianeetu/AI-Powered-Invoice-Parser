from paddleocr import PaddleOCR
import cv2
import numpy as np

ocr = PaddleOCR(use_angle_cls=True, lang='en')

def extract_text_from_images(images):
    final_text = []

    for image in images:
        img_array = image if isinstance(image, np.ndarray) else cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)
        result = ocr.ocr(img_array, cls=True)
        if result:
            for line in result[0]:
                text = line[1][0].strip()
                if text:
                    final_text.append(text)

    merged_lines = []
    current_item = ""

    for line in final_text:
        lower = line.lower()
        if any(char.isdigit() for char in line) and ('rs' in lower or '₹' in lower or '.' in line):
            current_item += " " + line
            merged_lines.append(current_item.strip())
            current_item = ""
        else:
            current_item += " " + line

    if current_item:
        merged_lines.append(current_item.strip())

    return "\n".join(merged_lines)