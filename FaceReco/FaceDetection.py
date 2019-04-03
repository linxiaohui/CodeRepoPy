# -*- coding: utf-8 -*-
'''
人脸检测，将一个目录下的图片进行人脸识别并保存为同名+后缀的文件
'''
import os

import numpy as np
import cv2

face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")
testdata = r""
factor=1

for p in os.listdir(testdata):
    print(p)
    print(os.sep.join([testdata, p]))
    img = cv2.imread(os.sep.join([testdata, p]))
    img = cv2.resize(img, None, fx=factor, fy=factor, interpolation=cv2.INTER_CUBIC)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, 1.3, 5)
    for (x,y,w,h) in faces:
        img = cv2.rectangle(img,(x,y),(x+w,y+h),(255,0,0),2)
    cv2.imshow('img',img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
