# -*- coding: utf-8 -*- 
'''
Created on 2014-1-3

@author: GroundMelon
'''
import cv2
import math
import numpy as np

COLORWHITE = (255, 255, 255)
COLORBLACK = (0, 0, 0)
COLORLIGHTBLUE = (255, 0, 0)
COLORWINDOWDEFAULT = (240,240,240)


class AttitudeDisplay(object):
    def __init__(self):
        import os
        path = os.getcwd()
        if path.find('attitude') < 0:
            path+=r'\attitude'
        self.im_panel = cv2.imread(r'%s\panel.bmp'%path )
        self.im_pmask = cv2.imread(r'%s\pmask.bmp'%path, 0)
        self.im_empty = cv2.imread(r'%s\empty.bmp'%path )
    
        # --------- test ------------ 
        self.count = -1
        self.pitch = []
        self.roll = []
        self.yaw = []
        lst = range(0, 60, 5) + range(60, -60, -5) + range(-60,0,5)
        
        
        for i in lst:
            self.pitch.append(i)
            self.roll.append(0)
            self.yaw.append(0)
        for i in lst:
            self.pitch.append(0)
            self.roll.append(i)
            self.yaw.append(0)
         
        self.lstlen = len(lst*2)
        return None
            
    def test(self):
        self.count = (self.count + 1) % self.lstlen
        #print(self.count, self.pitch[self.count],self.roll[self.count],self.yaw[self.count])
        return self.generate_attitude_bitmap(self.pitch[self.count],
                                             self.roll[self.count],
                                             self.yaw[self.count],
                                             is_radius = False
                                             )
                                             
        
    def generate_attitude_bitmap(self, pitch, roll, yaw, is_radius = True):
        if not is_radius:
            pitch = pitch * math.pi / 180
            roll = roll * math.pi / 180
            yaw = yaw * math.pi / 180
        
        # 防止tan(theta)出现无限大，需要进行处理
        def deal_with_90_degree(theta):
            if abs(theta - math.pi/2) < 0.01:
                return theta * 0.98
            else:
                return theta
        
        pitch = deal_with_90_degree(pitch)
        roll = deal_with_90_degree(roll)
        yaw = deal_with_90_degree(yaw)
            
        im_fill = self.im_empty.copy()
        im_fill[:,:] = COLORWINDOWDEFAULT
        roll_dh = 50 * math.tan(roll)
        pitch_dh = pitch / (math.pi/2) * 40
        pts = np.array([[0, 50 + roll_dh + pitch_dh],      # left top point
                        [100, 50 - roll_dh + pitch_dh],    # right top point
                        [100,100],       # right bottom point
                        [0,100]          # left bottom
                       ], dtype = 'int32')
        
        cv2.fillConvexPoly(im_fill, pts, COLORLIGHTBLUE)
        
        mask = np.equal(self.im_pmask,255)
        im_rst = self.im_panel.copy()
        im_rst[mask] = im_fill[mask]
        
        #imgdata = cv2.cvtColor(np.uint8(im_rst), cv2.cv.CV_BGR2RGB)   

        return im_rst#(imgdata.shape[1], imgdata.shape[0], imgdata)

if __name__ == '__main__':
    attidisp = AttitudeDisplay()
    attidisp.generate_attitude_bitmap(-10, 30, 0, is_radius = False)