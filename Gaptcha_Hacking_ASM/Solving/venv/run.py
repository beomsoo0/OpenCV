import numpy as np
import cv2
import utils
import requests
import shutil
import time



FILE_NAME = 'trained.npz'

with np.load(FILE_NAME) as data:
    train = data['train']
    train_labels = data['train_labels']

knn = cv2.ml.KNearest_create()
knn.train(train, cv2.ml.ROW_SAMPLE, train_labels)      # 학습시킴


# 가장 가까운 K개의 글자 찾기
def check(test, train, train_labels):

    ret, result, neighbours, dist = knn.findNearest(test, k=1)
    return result

def get_result(file_name):
    image = cv2.imread(file_name)
    chars = utils.extract_chars(image)
    result_string = ""

    for char in chars:
        matched = check(utils.resize20(char[1]), train, train_labels)
        if matched < 10:
            result_string += str(int(matched))
            continue
        if matched == 10:
            matched = '+'
        elif matched == 11:
            matched = '-'
        elif matched == 12:
            matched = '*'
        result_string += matched
    return result_string

print(get_result("image_2.png"))


host = "http://localhost:10000"
url = '/start'

with requests.Session() as s:
    answer = ''
    for i in range(0, 100):
        start_time = time.time()
        params = {'ans':answer}

        # 정답을 파라미터에 담아 전송, 이미지 경로 받아오기
        response = s.post(host+url, params)
        print('Server Return :', response.text)
        if i == 0:          # 처음 (start에 대한 요청)
            returned = response.text
            image_url = host + returned
            url = '/check'
        else:
            returned = response.json()       # 처음 아니면 json 형태로옴
            image_url = host + returned['url']

        print('Problem' + str(i) + ':' + image_url)

        # 이미지파일다운
        response = s.get(image_url, stream = True)
        target_image = './target_images/' + str(i) + '.png'
        with open(target_image, 'wb') as out_file:
            shutil.copyfileobj(response.raw, out_file)
        del response


        # 다운받은 이미지로 답 도출
        answer_string = get_result(target_image)
        print('String : ' + answer_string)
        answer_string = utils.remove_first_0(answer_string)
        answer = str(eval(answer_string))
        print('Answer: ' + answer)
