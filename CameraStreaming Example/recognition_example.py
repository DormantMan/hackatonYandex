import os

import cv2 as cv
import numpy as np

cap = cv.VideoCapture(0)


def persentage(image, lower, upper, stop, text):
    thresh = cv.inRange(hsv, lower, upper)

    size = (100, 100)

    thresh = cv.erode(thresh, None, iterations=2)
    thresh = cv.dilate(thresh, None, iterations=4)

    contours = cv.findContours(thresh.copy(), cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)
    contours = contours[1]

    if not contours:
        return

    c = sorted(contours, key=cv.contourArea, reverse=True)[0]
    rect = cv.minAreaRect(c)
    box = np.int0(cv.boxPoints(rect))
    cv.drawContours(frame, [box], -1, (0, 255, 0), 3)  # draw contours in green color

    y1 = int(box[0][1])
    x2 = int(box[1][0])
    y2 = int(box[1][1])
    x3 = int(box[2][0])

    roiImg = frame[y2:y1, x2:x3]

    if roiImg.any():
        cv.imshow('roiImg', roiImg)
        resizedRoi = cv.resize(roiImg, size)
        xresizedRoi = cv.inRange(resizedRoi, lower, upper)
        yet = cv.inRange(cv.resize(cv.imread(os.path.join('img', image)), size), lower, upper)

        res = 0
        for i in range(size[0]):
            for j in range(size[1]):
                if xresizedRoi[i][j] == yet[i][j]:
                    res += 1

        if image == 'giveWay.png':
            print(res, text)

        if res > stop:
            print(res, text)
            return True

    cv.imshow('frame', frame)

    return False


while True:
    ret, frame = cap.read()
    hsv = cv.cvtColor(frame, cv.COLOR_BGR2HSV)

    hsv = cv.blur(hsv, (5, 5))

    images = {
        'noDrive.png': [np.array([119, 101, 73]), np.array([255, 255, 255]), 5500, 'Езда запрещена'],
        'mainRoad.png': [np.array([0, 24, 100]), np.array([255, 255, 255]), 8200, 'Главная дорога'],
        'entryStop.png': [np.array([119, 101, 73]), np.array([255, 255, 255]), 10 ** 24, 'Проезда нет'],

        'giveWay.png': [np.array([0, 101, 73]), np.array([255, 255, 255]), 10 ** 24, 'Уступи дорого'],
        'parking.png': [np.array([0, 101, 73]), np.array([255, 255, 255]), 10 ** 24, 'Парковка'],
        'pedestrain.png': [np.array([0, 101, 73]), np.array([255, 255, 255]), 10 ** 24, 'Пешеходный переход'],

        'roadWorks.png': [np.array([0, 101, 73]), np.array([255, 255, 255]), 10 ** 24, 'Дорожные работы'],
        'speedBump.png': [np.array([0, 101, 73]), np.array([255, 255, 255]), 10 ** 24, 'Лежачий полицейский'],
        'stopSign.png': [np.array([0, 101, 73]), np.array([255, 255, 255]), 10 ** 24, 'Знак остановки'],
    }

    for name, data in images.items():
        lower, upper, stop, text = data
        flag = persentage(name, lower, upper, stop, text)

    cv.imshow('frame', frame)

    if cv.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv.destroyAllWindows()
