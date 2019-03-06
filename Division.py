# -*- coding: UTF-8 -*-
import cv2
import os
import numpy as np
import time

os.chdir(os.path.dirname(__file__))
def spite(b_img):
    '''cv2.findContours()函数接受的参数为二值图，即黑白的（不是灰度图），
    所以读取的图像要先转成灰度的，再转成二值图
    这个函数实际上返回了三个值
    第一个，它返回了你所处理的图像
    第二个，返回我们要找的轮廓集list，list元素为轮廓点集坐标构成的矩阵
    第三个，各层轮廓的索引'''
    binary, contours, hierarchy = cv2.findContours(b_img, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    print("轮廓数量：",type(contours), len(contours))  # 共几个轮廓
    print("第一个轮廓的点集个数", len(contours[0]))  # 第一个轮廓的点集个数
    print("第一个轮廓的坐标集",contours[0])  # 第一个轮廓的坐标集
    print("第一个轮廓的面积",cv2.contourArea(contours[0]))  # 第一个轮廓的面积

    '''第一个参数是指明在哪幅图像上绘制轮廓；
    第二个参数是轮廓本身，在Python中是一个list。
    第三个参数指定绘制轮廓list中的哪条轮廓，如果是-1，则绘制其中的所有轮廓。
    第四个参数表示颜色
    第五个参数表示轮廓线的宽度，如果是-1，则为填充模式'''
    #cv2.drawContours(img,contours,-1,(0,0,255),2)
    #cv2.imshow("img", img)

    #cv2.contourArea计算轮廓面积,返回轮廓内像素点的个数，此处将轮廓集按面积排序
    c = sorted(contours, key=cv2.contourArea, reverse=True)
    if len(c)<4:
        return
    for m in c[0:4]:
        # cv2.minAreaRect主要求得包含点集最小面积的矩形，这个矩形是可以有偏转角度的，可以与图像的边界不平行。
        rect = cv2.minAreaRect(m)
        print(type(rect), rect)
        box = np.int0(cv2.boxPoints(rect))
        print(box)
        


        #cv2.drawContours(binary, [box], -1, (0, 255, 0), 3)
        #cv2.imshow("largest shape", binary)
        
        #box倾斜的角度
        angle=rect[-1]
        if abs(angle)>45:
            angle=90-abs(angle)
        #box中心
        center=(box[0]+box[1]+box[2]+box[3])/4
        if abs(box[0][1]-box[1][1])<abs(box[1][1]-box[2][1]):
            x1=box[0][0]
            y1=box[0][1]
            x2=box[1][0]
            y2=box[1][1]
            width = np.sqrt(np.sum(np.square(box[0] - box[1])))
            high = np.sqrt(np.sum(np.square(box[1] - box[2])))
        else:
            x1=box[1][0]
            y1=box[1][1]
            x2=box[2][0]
            y2=box[2][1]
            width = np.sqrt(np.sum(np.square(box[1] - box[2])))
            high = np.sqrt(np.sum(np.square(box[2] - box[3])))
            
        
        print("width, high, angle",width, high, angle)

        # 第一个参数旋转中心，第二个参数旋转角度，第三个参数：缩放比例
        M = cv2.getRotationMatrix2D((center[0], center[1]), angle, 1)
        # 第三个参数：变换后的图像大小
        res = cv2.warpAffine(binary, M, (240, 110))
        #cv2.imshow("img2", res)

        # 裁剪图片
        x1 = int(center[0] - width/2)
        y1 = int(center[1] - high/2)
        x2 = int(center[0] + width/2)
        y2 = int(center[1] + high/2)
        print("x1,y1",x1, y1)
        print("x2,y2",x2, y2)
        res = res[y1:y2, x1:x2]
        #cv2.imshow("img3", res)

        #创建全黑图像
        s_img=np.zeros((80, 75), dtype=np.uint8)
        try:
            s_img[:res.shape[0],:res.shape[1]]=res
        except BaseException as e:
            print('错误信息是:', e)
            cv2.imwrite("binaryR.jpg",b_img)
            return

        #反色
        s_img = cv2.bitwise_not(s_img)
        
        cv2.imwrite("data\\"+str(time.time())+".jpg", s_img)
        cv2.waitKey(0)


if __name__=="__main__":
    img = cv2.imdecode(np.fromfile('edge.png', dtype=np.uint8), 1)
    # 图片先转成灰度的
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # 再把图片转换为二值图
    ret, binary = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY)
    
    # 图片反色
    binary = cv2.bitwise_not(binary)
    spite(binary)
