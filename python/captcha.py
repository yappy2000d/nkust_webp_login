from io import BytesIO

import cv2
import glob
import numpy as np
from PIL import Image

datas_path = glob.glob("../images/bmp/*.bmp")
data = [cv2.imread(x)[:, :, 0] for x in datas_path]

KEY = "123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ"


def recognize(image: BytesIO) -> str:
    img_array = np.array(Image.open(image))
    img_gray = cv2.cvtColor(img_array, cv2.COLOR_BGR2GRAY)

    morph_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (5, 5))

    _, img_binary = cv2.threshold(img_gray, 0, 255, cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)
    img_final = cv2.morphologyEx(img_binary, cv2.MORPH_CLOSE, morph_kernel)

    contours, _ = cv2.findContours(img_binary, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    results = []  # 切割後的結果
    for item in contours:
        rect = cv2.boundingRect(item)
        x, y, w, h = rect
        results.append([x, img_final[y:y + h, x:x + w]])

    if len(results) != 4:
        raise Exception("字元切割失敗")

    results = sorted(results, key=lambda x: x[0])

    input_images: list[np.ndarray] = [item[1] for item in results]
    ans = ""

    for a in input_images:
        score = [0] * (9 + 26)  # 0~9 + A~Z（因為 O 與 0 容易搞混，所以沒有 0）
        for i, b in enumerate(data):
            a = cv2.copyMakeBorder(a, 0, 30 - a.shape[0], 0, 30 - a.shape[1], cv2.BORDER_CONSTANT, 0)
            b = cv2.copyMakeBorder(b, 0, 30 - b.shape[0], 0, 30 - b.shape[1], cv2.BORDER_CONSTANT, 0)
            score[i] = sum(np.sqrt(sum(pow(a - b, 2))))

        ans += KEY[np.argmin(score)]

    return ans
