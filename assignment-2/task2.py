"""
Task #2

Зробити розпізнавання використовуючи будь-яке відео з обличчям людини,
тривалiстю не менше 30 секунд. Можно використати камеру ноутбука

"""

import cv2
from config import Config
from cascades import face_cascade, eye_cascade, smile_cascade


cap = cv2.VideoCapture(0)

while 1:
    ret, img = cap.read()
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, Config.scaling_factor, Config.min_neighbors)

    for (x, y, w, h) in faces:
        cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 0), 2)
        roi_gray = gray[y:y + h, x:x + w]
        roi_color = img[y:y + h, x:x + w]

        eyes = eye_cascade.detectMultiScale(roi_gray)
        for (ex, ey, ew, eh) in eyes:
            cv2.rectangle(roi_color, (ex, ey), (ex + ew, ey + eh), (0, 255, 0), 2)

        # smiles = smile_cascade.detectMultiScale(roi_gray)
        # for (sx, sy, sw, sh) in smiles:
        #     cv2.rectangle(roi_color, (sx, sy), (sx + sw, sy + sh), (0, 0, 255), 2)

    cv2.imshow('img', img)
    k = cv2.waitKey(30) & 0xff
    if k == 27:
        break

cap.release()
cv2.destroyAllWindows()