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

def create_needed_files():
    img = cv2.imread('empty.bmp')
    img[:,:,:]=255
    r=40
    l=4
    linewidth = 1
    cv2.circle(img, (50,50), r, COLORBLACK, linewidth)
    for i in range(0, 360, 30):
        if i not in [0,90,180,270]:
            xt = i * math.pi / 180
            dot1 = (int(50 + math.cos(xt)*(r-l)) , int(50 + math.sin(xt)*(r-l)) )
            dot2 = (int(50 + math.cos(xt)*(r-1)) , int(50 + math.sin(xt)*(r-1)) )
            cv2.line(img, dot1, dot2, (0,0,0), linewidth)
    
    cv2.line(img, (50, 50-(r-1)), (50, 50+(r-1)), COLORBLACK, linewidth)
    cv2.line(img, (50-(r-1), 50), (50+(r-1), 50), COLORBLACK, linewidth)
    
    cv2.imwrite('panel.bmp', img)
    
    img = cv2.imread('empty.bmp')
    cv2.circle(img, (50,50), r-linewidth, COLORWHITE, -1)
    for i in range(0, 360, 30):
        if i not in [0,90,180,270]:
            xt = i * math.pi / 180
            dot1 = (int(50 + math.cos(xt)*(r-l)) , int(50 + math.sin(xt)*(r-l)) )
            dot2 = (int(50 + math.cos(xt)*(r-1)) , int(50 + math.sin(xt)*(r-1)) )
            cv2.line(img, dot1, dot2, COLORBLACK, linewidth)
    
    cv2.line(img, (50, 50-(r-1)), (50, 50+(r-1)), COLORBLACK, linewidth)
    cv2.line(img, (50-(r-1), 50), (50+(r-1), 50), COLORBLACK, linewidth)
    cv2.imwrite('pmask.bmp', img)

class AttitudeBitmap(object):
    def __init__(self):
        self.im_panel = cv2.imread('panel.bmp')
        self.im_pmask = cv2.imread('pmask.bmp', 0)
        self.im_empty = cv2.imread('empty.bmp')

    def generate_attitude_bitmap(self, pitch, roll, yaw, is_radius = True):
        if not is_radius:
            pitch = pitch * math.pi / 180
            roll = roll * math.pi / 180
            yaw = yaw * math.pi / 180
        
        def deal_with_90_degree(theta):
            if abs(theta - math.pi/2) < 0.01:
                return theta * 0.98
            else:
                return theta
        
        pitch = deal_with_90_degree(pitch)
        roll = deal_with_90_degree(roll)
        yaw = deal_with_90_degree(yaw)
            
        im_fill = self.im_empty.copy()
        im_fill[:,:] = COLORWHITE
        roll_dh = 40 * math.tan(roll)
        pitch_dh = 50 * math.tan(pitch)
        pts = np.array([[0, 50 + roll_dh + pitch_dh],      # left top point
                        [100, 50 - roll_dh + pitch_dh],    # right top point
                        [100,100],       # right bottom point
                        [0,100]          # left bottom
                       ], dtype = 'int32')
        
        cv2.fillConvexPoly(im_fill, pts, COLORLIGHTBLUE)
        
        mask = np.equal(self.im_pmask,255)
        im_rst = self.im_panel.copy()
        im_rst[mask] = im_fill[mask]
            
        imgdata = cv2.cvtColor(np.uint8(im_rst), cv2.cv.CV_BGR2RGB)
        return (imgdata.shape[1], imgdata.shape[0], imgdata)
    
if __name__ == '__main__':
    create_needed_files()
    attbmp = AttitudeBitmap()
    attbmp.generate_attitude_bitmap(-10, 30, 0, is_radius = False)
    