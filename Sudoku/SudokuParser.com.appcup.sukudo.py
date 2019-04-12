# -*- coding: UTF-8 -*-

sudoku_img = 'data\\Screenshot_2019-01-13-03-55-33-977_com.appcup.sukudo.png'

import cv2

def FindCOI(inpath):
    image = cv2.imread(inpath)
    width, height, color = image.shape
    print(width, height, color)
    cv2.namedWindow("COI")

    def onMouse(evt, x, y, flags, param):
        if evt == cv2.EVENT_LBUTTONDOWN:
            param["drawing"]=True
            param["start_pos"]=(x,y)
        elif evt == cv2.EVENT_MOUSEMOVE and flags&cv2.EVENT_FLAG_LBUTTON:
            param["curr_pos"]=(x,y)
            if param["drawing"]:
                frame = cv2.rectangle(image.copy(), param["start_pos"], (x, y), (0, 255, 0), 0)
                cv2.imshow(inpath, frame)
        elif evt == cv2.EVENT_LBUTTONUP:
            (x1, y1)=param["start_pos"]
            (x2, y2)=param["curr_pos"]
            X=min(x1,x2)
            Y=min(y1,y2)
            W=max(x1-x2,x2-x1)
            H=max(y1-y2,y2-y1)
            print(X,Y,W,H)

    param = {}
    cv2.setMouseCallback("COI", onMouse, param)
    cv2.imshow("COI", image)
    cv2.waitKey(0)
    
FindCOI(sudoku_img)