# -*- coding: utf-8 -*- 
'''
Created on 2014-3-22

@author: GroundMelon
'''
import cv2
import util

class Record(object):
    def __init__(self, path, fps, size):
        fourcc = cv2.VideoWriter_fourcc('X','D','I','V')
        self.out = cv2.VideoWriter(path, -1, fps, size)
    
    def save_frame(self, wxbmp):
        frame = util.wxbmp_to_cvimg(wxbmp)
        self.out.write(frame)
    
    def stop(self):
        self.out.release()