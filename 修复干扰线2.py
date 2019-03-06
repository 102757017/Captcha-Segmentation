# -*- coding: UTF-8 -*-
import numpy as np
from PIL import Image
import os
import cv2
import numpy as np
import scipy.ndimage as ndimg


os.chdir(os.path.dirname(__file__))
# 由于opencv不支持读取中文路径，用以下方法代替cv2.imread
frame = cv2.imdecode(np.fromfile('re_color.png', dtype=np.uint8), 1)

 
# 把 BGR 转为 HSV
hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
 

#opencv中，H（色度）范围[0,255],S(饱和度)范围[0,255]，V(亮度)范围[0,115]
lower_blue = np.array([0,0,0]) 
upper_blue = np.array([255,255,115]) 
 
# 获得区域的mask
mask = cv2.inRange(hsv, lower_blue, upper_blue)

h_structure = cv2.getStructuringElement(cv2.MORPH_RECT, (1, 3))
#膨胀mask
mask = cv2.dilate(mask, h_structure, 1)

rr, cc = ndimg.distance_transform_edt(mask, return_distances=False, return_indices=True)
img = frame[rr, cc]
cv2.imshow('img',img)
cv2.imwrite("repair.png",img)
