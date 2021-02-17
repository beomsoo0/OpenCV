import os
import cv2
import utils

image = cv2.imread('image_3.png')
chars = utils.extract_chars(image)

# training_data 폴더 생성 및 내부에 0 ~ 12 폴더 생성
for char in chars:
    cv2.imshow('image', char[1])
    input = cv2.waitKey(0)
    resized = cv2.resize(char[1], (20, 20))

    # 숫자 0~9 레이블 생성  (아스키코드 48 = 0, 57 = 9)
    if input >= 48 and input <= 57:
        name = str(input - 48)
        file_count = len(next(os.walk('./training_data/' + name + '/'))[2])
        cv2.imwrite('./training_data/' + name + '/' +
                    str(file_count + 1) + '.png', resized)

    # +, -, * => a, b, c로 입력하여 10, 11, 12에 저장
    elif input == ord('a') or ord('b') or ord('c'):
        name = str(input - ord('a') + 10)
        file_count = len(next(os.walk('./training_data/' + name + '/'))[2])
        cv2.imwrite('./training_data/' + name + '/' +
                    str(file_count + 1) + '.png', resized)