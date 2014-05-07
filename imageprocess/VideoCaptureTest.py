# -*- coding: utf-8 -*- 
'''
Created on 2014-3-15

@author: GroundMelon
'''
from VideoCapture import Device
import cv2
import numpy as np
import time

if __name__ =='__main__':
    # test two methods
    cam = Device(devnum=0)
    cam.displayCaptureFilterProperties()
    cam.displayCapturePinProperties()
    
    a=time.clock()
    im_pil = cam.getImage().convert('RGB') 
    for i in range(1):
        s = im_pil.tostring()
        cvimg = np.ndarray(shape = (im_pil.size[1],im_pil.size[0],3), dtype = np.uint8, buffer = s)
        cvimg = cvimg[:,:,::-1]#.copy()
        #cv2.imshow('',cvimg)
        #cv2.waitKey(100)
    print('DxShow-mmap:%s'%(str((time.clock()-a)/1000.0)))
    
    for i in range(1000):
        im_pil = cam.getImage().convert('RGB') 
        cvimg = np.array(im_pil)
        cvimg = cvimg[:,:,::-1]
    print('DxShow-direct:%s'%(str((time.clock()-a)/1000.0)))
    del cam
    
    cap = cv2.VideoCapture('test.mp4')
    a = time.clock()
    for i in range(100):
        _, cvimg = cap.read()
        #s = cvimg.tostring()
        #img = np.ndarray(shape = cvimg.shape, dtype = cvimg.dtype, buffer = s)
        cv2.imshow('',cvimg)
        cv2.waitKey(100)
    print('Cv:%s'%(str((time.clock()-a)/100.0)))
    cap.release()

#------------- save avi -----------

#     cap = cv2.VideoCapture(0)
#      
#     fourcc = cv2.VideoWriter_fourcc(*'MJPG')
#     # Define the codec and create VideoWriter object
#     out = cv2.VideoWriter('output.avi', -1, 20.0, (640,480))
#      
#     while(cap.isOpened()):
#         ret, frame = cap.read()
#         if ret==True:
#             frame = cv2.flip(frame,0)
#      
#             # write the flipped frame
#             out.write(frame)
#      
#             cv2.imshow('frame',frame)
#             if cv2.waitKey(1) & 0xFF == ord('q'):
#                 break
#         else:
#             break
#      
#     # Release everything if job is finished
#     cap.release()
#     out.release()
#     cv2.destroyAllWindows()
