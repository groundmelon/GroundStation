# -*- coding: utf-8 -*- 
'''
Created on 2014-3-15

@author: GroundMelon
'''
from VideoCapture import Device
import cv2
import numpy as np

cam = Device()
#cam.displayCaptureFilterProperties()
cam.displayCapturePinProperties()
im_pil = cam.getImage().convert('RGB')
cvimg = np.array(im_pil)
cvimg = cvimg[:,:,::-1].copy()
cv2.imshow('',cvimg)

while True:
    import time
    a=time.clock()
    im_pil = cam.getImage().convert('RGB')
    cvimg = np.array(im_pil)
    cvimg = cvimg[:,:,::-1]#.copy()
    cv2.imshow('',cvimg)
    #cv2.waitKey(100)
    print(str(time.clock()-a))
del cam