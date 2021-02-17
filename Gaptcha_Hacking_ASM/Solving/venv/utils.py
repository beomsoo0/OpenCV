import cv2
import numpy as np
import re

BLUE = 0
GREEN = 1
RED = 2

def get_chars(image, color):

    other_1 = (color + 1) % 3
    other_2 = (color + 2) % 3

    c = image[:, :, other_1] == 255     # other_1 값이 255(FF)라면
    image[c] = [0, 0, 0]

    c = image[:, :, other_2] == 255     # other_2 값이 255(FF)라면
    image[c] = [0, 0, 0]

    c = image[:, :, color] < 170        # color 값이 170(AA)보다 작다면 (other_1 && other_2)
    image[c] = [0, 0, 0]

    c = image[:, :, color] != 0         # color 존재 부분
    image[c] = [255, 255, 255]

    return image;


def extract_chars(image):
    chars = []
    colors = [BLUE, GREEN, RED]

    # contour 찾기 위해 gray로 바꾼 후 thresholding
    for color in colors:
        image_from_one_color = get_chars(image.copy(), color)
        image_gray = cv2.cvtColor(image_from_one_color, cv2.COLOR_BGR2GRAY)
        ret, thresh = cv2.threshold(image_gray, 127, 255, 0)
        contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        for contour in contours:
            area = cv2.contourArea(contour)
            if area > 50:                                               # 크기 작은 contour 해당 x
                x, y, width, height = cv2.boundingRect(contour)
                roi = image_gray[y:y+height, x:x+width]
                chars.append((x, roi))

    chars = sorted(chars, key=lambda char : char[0])                    # char[0] (x좌표) 기준 오름차순 정렬
    return chars

# 20x20으로 resizing 후 1차원 배열로 바꿈
def resize20(image):
    resized = cv2.resize(image, (20, 20))
    return resized.reshape(-1, 400).astype(np.float32)


# eval()로 반환하기 위해 왼쪽 0 지우기
def remove_first_0(string):
    temp = []
    for i in string:
        if i == '+' or i == '-' or i == '*':
            temp.append(i)
    split = re.split('\*|\+|\-', string)
    i = 0
    temp_count = 0
    result = ""
    for a in split:
        a = a.lstrip("0")
        if a == '':
            a == '0'
        result += a

        if i < len(split) - 1:
            result += temp[temp_count]
            temp_count += 1
        i = i + 1
    return result
