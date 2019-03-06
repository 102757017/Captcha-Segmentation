# -*- coding: UTF-8 -*-
import cv2
import os
import numpy as np
from Binary import black
from Repair import repair
from Division import spite
from Crab import get_captcha

if __name__=="__main__":
    os.chdir(os.path.dirname(__file__))
    i=1
    while i<500:
        frame=get_captcha()
        img=repair(frame)
        img=black(img)
    
        # 图片反色
        img = cv2.bitwise_not(img)
        spite(img)
        #cv2.imshow("image3",img)
        i=i+1
