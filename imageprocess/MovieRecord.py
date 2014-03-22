# -*- coding: utf-8 -*- 
'''
Created on 2014-3-22

@author: GroundMelon
'''
import cv2

class Record(object):
    def __init__(self, path, fps, size):
        #fourcc = cv2.cv.FOURCC('M', 'J', 'P', 'G')
        self.out = cv2.VideoWriter(path, 0, fps, size)
    
    def save_frame(self, frame):
        self.out.write(frame)
    
    def stop(self):
        self.out.release()