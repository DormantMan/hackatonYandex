import os

import cv2 as cv
import numpy as np

cap = cv.VideoCapture(0)

MIN_REC = 2400

def percentage(image, lower, upper, stop, text):
    thresh = cv.inRange(hsv, lower, upper)

    size = 64, 64

    thresh = cv.erode(thresh, None, iterations=2)
    thresh = cv.dilate(thresh, None, iterations=4)

    contours = cv.findContours(thresh.copy(), cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)
    contours = contours[1]

    if not contours:
        return

    height, width = thresh.shape
    min_x, min_y = width, height
    max_x = max_y = 0

    for _ in range(1):  # sorted(contours, key=cv.contourArea)[-1]
        c = sorted(contours, key=cv.contourArea)[-1]
        rect = cv.minAreaRect(c)

        yet = 100

        if rect[0][0] < yet or rect[0][1] < yet or rect[1][0]  < yet or rect[1][1] < yet:
            continue

        box = np.int0(cv.boxPoints(rect))
        cv.drawContours(frame, [box], -1, (0, 255, 0), 3)  # draw contours in green color

        # Выделение части, на которой расположен знак из изображении
        (x, y, w, h) = cv.boundingRect(c)
        min_x, max_x = min(x, min_x), max(x + w, max_x)
        min_y, max_y = min(y, min_y), max(y + h, max_y)
        roiImg = frame[min_y:max_y, min_x:max_x]

        if roiImg.any():
            resizedRoi = cv.resize(roiImg, size)
            xresizedRoi = cv.inRange(resizedRoi, lower, upper)
            yet = cv.inRange(cv.resize(cv.imread(os.path.join('img', image)), size), lower, upper)

            res = 0
            for i in range(size[0]):
                for j in range(size[1]):
                    if xresizedRoi[i][j] == yet[i][j]:
                        res += 1

            if res > stop:
                cv.putText(frame, image, (20, 20), cv.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 255), 2)
                out.write(frame)
                cv.imshow('frame', frame)
                return True
    return False


fourcc = cv.VideoWriter_fourcc(*'XVID')
out = cv.VideoWriter('output.avi', fourcc, 30.0, (640, 480))
images = {
        'noDrive.png': [np.array([0, 110, 0]), np.array([15, 255, 255]), MIN_REC, 'Езда запрещена'],
        'mainRoad.png': [np.array([10, 130, 120]), np.array([60, 255, 255]), MIN_REC, 'Главная дорога'],
        'entryStop.png': [np.array([0, 110, 0]), np.array([15, 255, 255]), MIN_REC, 'Въезд запрещен'],

        'giveWay.png': [np.array([0, 110, 0]), np.array([15, 255, 255]), MIN_REC, 'Уступи дорогу'],
        'parking.png': [np.array([100, 110, 140]), np.array([140, 255, 255]), MIN_REC, 'Парковка'],
        'pedestrain.png': [np.array([90, 0, 0]), np.array([140, 255, 110]), MIN_REC, 'Пешеходный переход'],

        'roadWorks.png': [np.array([10, 130, 120]), np.array([60, 255, 255]), MIN_REC, 'Дорожные работы'],
        'speedBump.png': [np.array([0, 110, 0]), np.array([15, 255, 255]), MIN_REC, 'Лежачий полицейский'],
        'stopSign.png': [np.array([0, 110, 0]), np.array([15, 255, 255]), MIN_REC, 'Знак остановки'],
}

while True:
    ret, frame = cap.read()
    hsv = cv.cvtColor(frame, cv.COLOR_BGR2HSV)

    hsv = cv.blur(hsv, (5, 5))

    for name, data in images.items():
        lower, upper, stop, text = data
        flag = percentage(name, lower, upper, stop, text)

    if cv.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv.destroyAllWindows()
