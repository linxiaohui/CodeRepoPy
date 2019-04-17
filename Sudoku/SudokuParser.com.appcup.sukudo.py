# -*- coding: UTF-8 -*-
# 根据【特定格式的】图片输入 提取数独
# 

import os
import glob

import cv2
import numpy as np

def FindSudukuMannually(inpath):
    image = cv2.imread(inpath)
    width, height, color = image.shape
    print(width, height, color)
    cv2.namedWindow("COI", cv2.WINDOW_NORMAL)
    def onMouse(evt, x, y, flags, param):
        if evt == cv2.EVENT_LBUTTONDOWN:
            param["drawing"]=True
            param["start_pos"]=(x,y)
        elif evt == cv2.EVENT_MOUSEMOVE and flags&cv2.EVENT_FLAG_LBUTTON:
            param["curr_pos"]=(x,y)
            if param["drawing"]:
                frame = cv2.rectangle(image.copy(), param["start_pos"], (x, y), (0, 255, 0), 0)
                cv2.imshow("COI", frame)
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
    
#FindCOI('data\\Screenshot_2019-01-13-03-55-33-977_com.appcup.sukudo.png')
X,Y,W,H = 125,172,836,830

def ClipToSudoku(in_path, out_path, X,Y,W,H):
    '''将图片的 X,Y,W,H 截取出来'''
    image = cv2.imread(in_path)
    coi = image[Y:Y+H,X:X+W]
    cv2.imwrite(out_path, coi)


def SliptToNum(sudoku_path, no):
    '''将sudoku图片拆分为9*9张图片数字'''
    image = cv2.imread(sudoku_path)
    hight, width, _ = image.shape
    hight_size = hight//9
    width_size = width//9
    seq = 0
    for i in range(0,9):
        for j in range(0,9):
            num = image[i*hight_size:i*hight_size+hight_size, j*width_size:j*width_size+width_size]
            cv2.imwrite("{}_{}.png".format(no,seq), num)
            seq+=1

TRAIN_DATA_PATH = 'train_data'
SUDOKU_IAMGES = 'sudoku_images'
INPUT_DATA_PATH = 'data'
    
def buildTrainData():   
    # 将输入数据中的所有图片，切出数独部分，并拆分为9*9的小文件
    fi = 0
    for f in glob.iglob(os.path.join(INPUT_DATA_PATH,"*")):
        print(f)
        fi+=1
        image = cv2.imread(f)
        coi = image[Y:Y+H,X:X+W]
        cv2.imwrite(os.path.join(SUDOKU_IAMGES,"{}.png".format(fi)), coi)
        hight, width, _ = coi.shape
        hight_size = hight//9
        width_size = width//9
        seq = 0
        for i in range(0,9):
            for j in range(0,9):
                num = coi[i*hight_size:i*hight_size+hight_size, j*width_size:j*width_size+width_size]
                #num = num[10:-10,10:-10]
                cv2.imwrite(os.path.join(TRAIN_DATA_PATH,"{}_{}.png".format(fi,seq)), num)
                seq+=1
#buildTrainData()

# 与本项目中DigitRecognition类似，试用cv2中自带KNN分类
def buildModel():
    # Features
    labels = list(range(0,10))
    samples =  np.empty((0,100),dtype=np.float32)
    responses = []
    for label in labels:
        for f in glob.iglob(os.path.join(TRAIN_DATA_PATH,str(label),"*")):
            im = cv2.imread(f)
            im = im[10:-10,5:-5]
            im = cv2.resize(im, None, fx=5,fy=5, interpolation=cv2.INTER_CUBIC)
            gray = cv2.cvtColor(im,cv2.COLOR_BGR2GRAY)
            roismall = cv2.resize(gray,(10,10))
            sample = roismall.reshape((1,100))
            sample = np.array(sample,np.float32)
            samples = np.append(samples,sample,0)
            responses.append(label)
    responses = np.array(responses,np.float32)
    responses = responses.reshape((responses.size,1))
    shuffle_ind = np.arange(len(responses))
    np.random.shuffle(shuffle_ind)
    samples = samples[shuffle_ind]
    responses = responses[shuffle_ind]
    split = int(len(responses)*0.8)
    # 建模
    model = cv2.ml.KNearest_create()
    model.train(samples[:split],cv2.ml.ROW_SAMPLE, responses[:split])
    error_cnt = 0
    for i in range(split,len(responses)):
        retval, results, neigh_resp, dists = MODEL.findNearest(samples[i].reshape(1,-1), k = 1)
        if responses[i]!=retval:
            error_cnt+=1
    print("建模完成,测试错误率", error_cnt, error_cnt/(len(responses)-split))
    return model


MODEL = buildModel()
    
def RecognizeDigit(im):
    '''输入原始（单个）图片，返回其数字
    None代表没有数字'''
    im = im[10:-10,5:-5]
    im = cv2.resize(im, None, fx=5,fy=5, interpolation=cv2.INTER_CUBIC)
    gray = cv2.cvtColor(im,cv2.COLOR_BGR2GRAY)
    roismall = cv2.resize(gray,(10,10))
    sample = roismall.reshape((1,100))
    sample = np.array(sample,np.float32)
    retval, results, neigh_resp, dists = MODEL.findNearest(sample, k = 1)
    return int(retval)

def BuildSudoku(image_path):
    '''输入应用截图的路径，输入Sudoku表示 (行,列,值) 的list'''
    sudoku_repr=[]
    image = cv2.imread(image_path)
    sudoku_image = image[Y:Y+H,X:X+W]
    hight, width, _ = sudoku_image.shape
    hight_size = hight//9
    width_size = width//9
    for i in range(0,9):
        for j in range(0,9):
            digit_image = sudoku_image[i*hight_size:i*hight_size+hight_size, j*width_size:j*width_size+width_size]
            digit = RecognizeDigit(digit_image)
            if digit:
                sudoku_repr.append((str(i+1),str(j+1), str(digit)))
    return sudoku_repr


sudoku = BuildSudoku('data\\Screenshot_2019-01-25-07-36-25-111_com.appcup.sukudo.png')
import SudokuSolver
v = SudokuSolver.SolveSudoku(sudoku)
SudokuSolver.SudokuPrint(v)