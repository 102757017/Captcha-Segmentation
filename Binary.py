# -*- coding: UTF-8 -*-
import cv2
import os
import numpy as np

def black(img):
    # 图片先转成灰度的
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # 给出高斯矩阵的尺寸和标准差，将图片进行高斯模糊
    # gray=cv2.GaussianBlur(gray, (3, 3), 0)

    # gray=cv2.Canny(gray,100,300)

    ret, binary = cv2.threshold(gray, 160, 255, cv2.THRESH_BINARY)
    return binary

if __name__=="__main__":
    os.chdir(os.path.dirname(__file__))
    # 由于opencv不支持读取中文路径，用以下方法代替cv2.imread
    img = cv2.imdecode(np.fromfile('binary.png', dtype=np.uint8), 1)
    img=black(img)
    cv2.imshow("image",img)
    print(img)
    cv2.imwrite("binary2.png",img)

