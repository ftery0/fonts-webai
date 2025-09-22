import cv2
import numpy as np
import os

def segment_template(image_path, out_dir="public/segments"):
    os.makedirs(out_dir, exist_ok=True)
    img = cv2.imread(image_path, cv2.IMREAD_COLOR)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    _, th = cv2.threshold(gray, 240, 255, cv2.THRESH_BINARY_INV)  # 배경 흰색 가정
    # 윤곽 검출
    contours, _ = cv2.findContours(th, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    boxes = [cv2.boundingRect(c) for c in contours]
    # 정렬 (top->bottom, left->right)
    boxes = sorted(boxes, key=lambda b: (b[1], b[0]))
    idx = 0
    for x,y,w,h in boxes:
        if w < 10 or h < 10: continue
        crop = gray[y:y+h, x:x+w]
        # 정규화: 정방형 캔버스에 중앙 정렬
        size = max(w,h)
        canvas = 255 * np.ones((size, size), dtype=np.uint8)
        xoff = (size - w)//2
        yoff = (size - h)//2
        canvas[yoff:yoff+h, xoff:xoff+w] = crop
        out_path = os.path.join(out_dir, f"seg_{idx:04d}.png")
        cv2.imwrite(out_path, canvas)
        idx += 1
    return idx
