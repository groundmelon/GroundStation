# -*- coding: utf-8 -*- 
'''
Created on 2014-3-15

@author: GroundMelon
'''
from VideoCapture import Device
import cv2
import numpy as np

# cam = Device(devnum=0)
# cam.displayCaptureFilterProperties()
# cam.displayCapturePinProperties()
# print('a')
# im_pil = cam.getImage().convert('RGB')
# print('b')
# cvimg = np.array(im_pil)
# cvimg = cvimg[:,:,::-1].copy()
# cv2.imshow('',cvimg)
# 
# while False:
#     import time
#     a=time.clock()
#     im_pil = cam.getImage().convert('RGB')
#     cvimg = np.array(im_pil)
#     cvimg = cvimg[:,:,::-1]#.copy()
#     cv2.imshow('',cvimg)
#     cv2.waitKey(100)
#     print(str(time.clock()-a))
# del cam

#------------- save avi -----------

cap = cv2.VideoCapture(0)

fourcc = cv2.VideoWriter_fourcc(*'MJPG')
# Define the codec and create VideoWriter object
out = cv2.VideoWriter('output.avi', -1, 20.0, (640,480))

while(cap.isOpened()):
    ret, frame = cap.read()
    if ret==True:
        frame = cv2.flip(frame,0)

        # write the flipped frame
        out.write(frame)

        cv2.imshow('frame',frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    else:
        break

# Release everything if job is finished
cap.release()
out.release()
cv2.destroyAllWindows()