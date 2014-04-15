# -*- coding: utf-8 -*- 
'''
Created on 2014-4-13

@author: GroundMelon
'''
# -*- coding: utf-8 -*- 
'''
Created on 2014-2-13

@author: GroundMelon
'''
import numpy as np
import cv2
import util

from Queue import Full as QFull
from Queue import Empty as QEmpty
import multiprocessing
from multiprocessing import Process
from multiprocessing import JoinableQueue
import os
import sys
import math

LINE_WIDTH = 5
DRAG_COLOR = (255,0,0)
OBJECT_MATCH_COLOR = (0, 0, 255)
SELECTPADDING = 10
# HUE_DELTA = 30
# SAT_DELTA = 30
# LIG_DELTA = 30
# MEDIANBLUR_KERNEL_SIZE = 5
# 
# MULTI_SPLIT_SCALE = 0.2
# 
CANNY_MIN = 100
CANNY_MAX = 200

class METHOD():
    TEMPLATEMATCH=0
    MEANSHIFT=1
    GRAYMEANSHIFT=2
    OPTICALFLOW=3

# ---- 图像调整相关函数 ----
def get_image_adjust_value():
    return {'Brightness':50, 'Contrast':50, 'Gamma':50}

def get_adjusted_image(src, image_adjust_value):
    dst = ((src * (image_adjust_value['Brightness']/50.0) 
            + (image_adjust_value['Contrast']-50)*2)
           **(image_adjust_value['Gamma']/50.0))                   
    # 把大于255的部分设置为255
    dst_255_mask = np.greater_equal(dst,255)
    dst[dst_255_mask] = 255
    return np.uint8(dst)

# ---- 框选相关函数 ----

def get_dragging_image(src, drag_data, bitmap_size):
    ''' 
    @param src: 源图像
    @param drag_data:拖拽数据 
    @param bitmap_size:显示区域的尺寸
    @return: 画框的图像
    ''' 
    img = src.copy()
    width = src.shape[1]
    height = src.shape[0]
    bw = bitmap_size[0] # bitmap width
    bh = bitmap_size[1] # bitmap height
    
    start = util.Point(drag_data['start'].x * width / bw, drag_data['start'].y * height / bh)
    end = util.Point(drag_data['end'].x * width / bw, drag_data['end'].y * height / bh)
    #left_top = util.Point(min(start.x, end.x), min(start.y, end.y))
    #right_down = util.Point(max(start.x, end.x), min(start.y, end.y))
    cv2.rectangle(img, start.tup, end.tup, DRAG_COLOR, LINE_WIDTH)
    return img

def get_selection_rect(src_size, drag_data, bitmap_size):
    ''' 
            获取框选区域在源图像上的左上角和右下角
    @param src_size: 源图像的尺寸
    @param drag_data:拖拽数据 
    @param bitmap_size:显示区域的尺寸
    @return: 画框的图像
    '''
    width  = src_size[1]
    height = src_size[0]
    bw = bitmap_size[0] # bitmap width
    bh = bitmap_size[1] # bitmap height
    
    start = util.Point(drag_data['start'].x * width / bw, drag_data['start'].y * height / bh)
    end = util.Point(drag_data['end'].x * width / bw, drag_data['end'].y * height / bh)
    left_top = util.Point(min(start.x, end.x), min(start.y, end.y))
    right_bottom = util.Point(max(start.x, end.x), max(start.y, end.y))
    return (left_top, right_bottom)

# ---- 跟踪方法类 ----
class TemplateMatch(object):
    def __init__(self, src, roi):
        self.object_template = roi
    
    def process(self, src, **kwargs):
        sw = util.SW('tpl-match')
        
        methods = ['cv2.TM_CCOEFF', 'cv2.TM_CCOEFF_NORMED', 'cv2.TM_CCORR',
            'c v2.TM_CCORR_NORMED', 'cv2.TM_SQDIFF', 'cv2.TM_SQDIFF_NORMED']
        method = eval(methods[0])
        res = cv2.matchTemplate(src, self.object_template, method)
        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)
        
        if method in [cv2.TM_SQDIFF, cv2.TM_SQDIFF_NORMED]:
            tl = min_loc
        else:
            tl = max_loc
            
        br = (tl[0] + self.object_template.shape[1], 
              tl[1] + self.object_template.shape[0]
              )
        center = ((tl[0]+br[0])/2, (tl[1]+br[1])/2)
        
        rst_img = src.copy()
        cv2.rectangle(rst_img,tl, br, OBJECT_MATCH_COLOR, LINE_WIDTH)
        rst_res = np.zeros(src.shape[0:2], dtype=np.uint8)
        rst_res = cv2.cvtColor(rst_res, cv2.COLOR_GRAY2BGR)
        cv2.putText(rst_res,'%f'%max_val, (0,rst_res.shape[0]), cv2.FONT_HERSHEY_SIMPLEX, 1, OBJECT_MATCH_COLOR)
        cv2.circle(rst_res, center, 3, OBJECT_MATCH_COLOR, LINE_WIDTH)
        
        sw. stop()
        return (rst_img, [util.Point(center)], rst_res)

class MeanShift(object):
    def __init__(self, src, roi, window, hist_channel=[0]):
        self.hist_channel = hist_channel
        hls_roi = cv2.cvtColor(roi, cv2.COLOR_BGR2HLS)
        mask = cv2.inRange(hls_roi, np.array((0., 0., 0.)), np.array((180.,255.,255.)))
        self.roi_hist = cv2.calcHist([hls_roi], self.hist_channel, mask, [180], [0,180])
        cv2.normalize(self.roi_hist, self.roi_hist, 0, 255, cv2.NORM_MINMAX)
        
        self.term_crit = (cv2.TERM_CRITERIA_EPS|cv2.TERM_CRITERIA_COUNT, 10, 1)
        self.track_window = window
        
    def process(self, src, **kwargs):         
        sw = util.SW('meanShift')
     
        hls = cv2.cvtColor(src, cv2.COLOR_BGR2HLS)
        dst = cv2.calcBackProject([hls], self.hist_channel, self.roi_hist, [0,180], 1)
        
        ret, window = cv2.meanShift(dst, self.track_window, self.term_crit)
        self.track_window = window
        x,y,w,h = window
        center = (int(x+w/2), int(y+h/2))
        rst_img = src.copy()
        cv2.rectangle(rst_img, (x,y), (x+w,y+h), OBJECT_MATCH_COLOR, LINE_WIDTH)
        prj_img = cv2.cvtColor(dst, cv2.COLOR_GRAY2BGR)
        cv2.rectangle(prj_img, (x,y), (x+w,y+h), OBJECT_MATCH_COLOR, LINE_WIDTH)
        
        sw.stop()
        return rst_img, [util.Point(center)], prj_img

class GrayMeanShift(object):    
    def __init__(self, src, roi, window):
        gray_roi = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)
#         mask = cv2.inRange(gray_roi, np.array((0.)), np.array((255.)))
        self.roi_gray_hist = cv2.calcHist([gray_roi], [0], None, [255], [0,255])
        cv2.normalize(self.roi_gray_hist, self.roi_gray_hist, 0, 255, cv2.NORM_MINMAX)
        
        self.term_crit = (cv2.TERM_CRITERIA_EPS|cv2.TERM_CRITERIA_COUNT, 10, 1)
        self.track_window = window
    
    def process(self, src,**kwargs):
        sw=util.SW('gray')
        
        gray = cv2.cvtColor(src, cv2.COLOR_BGR2GRAY)
        dst = cv2.calcBackProject([gray], [0], self.roi_gray_hist, [0,255], 1)
    
        ret, window = cv2.meanShift(dst, self.track_window, self.term_crit)
        self.track_window = window
        x,y,w,h = window
        center = (int(x+w/2), int(y+h/2))
        rst_img = cv2.cvtColor(gray, cv2.COLOR_GRAY2BGR)
        cv2.rectangle(rst_img, (x,y), (x+w,y+h), OBJECT_MATCH_COLOR, LINE_WIDTH)
        prj_img = cv2.cvtColor(dst, cv2.COLOR_GRAY2BGR)
        cv2.rectangle(prj_img, (x,y), (x+w,y+h), OBJECT_MATCH_COLOR, LINE_WIDTH)
        
        sw.stop()
        return rst_img, [util.Point(center)], prj_img

class OpticalFlow(object):    
    class ObjectMissError(Exception):
        pass
    def __init__(self, src, window):
        self.window = window
        self.set_init_status(src, window)
    
    def reinit(self, src, center):
        _,_,w,h = self.window
        self.set_init_status(src, (center.x-w/2, center.y-h[3]/2, w, h))
        
    def set_init_status(self, src, window):
        feature_params = dict( maxCorners = 100,
                       qualityLevel = 0.3,
                       minDistance = 20,
                       blockSize = 7 )
        x,y,w,h = window
        
#         x,y,w,h = (window[0]-SELECTPADDING, window[1]+SELECTPADDING*2, 
#                    window[2]-SELECTPADDING, window[3]+SELECTPADDING*2)
        
        self.old_gray = cv2.cvtColor(src, cv2.COLOR_BGR2GRAY)
#         self.opmask = np.zeros_like(self.old_gray, np.uint8)
#         self.opmask[x:x+w, y:y+h]=255
#         self.p0 = cv2.goodFeaturesToTrack(self.old_gray, mask = self.opmask, **feature_params)
        self.p0 = np.ndarray(shape=(9,1,2), dtype=np.float32)
        self.p0[0][0] = [x+w*1.0/4,y+h*1.0/4]
        self.p0[1][0] = [x+w*1.0/4,y+h*2.0/4]
        self.p0[2][0] = [x+w*1.0/4,y+h*3.0/4]
        self.p0[3][0] = [x+w*2.0/4,y+h*1.0/4]
        self.p0[4][0] = [x+w*2.0/4,y+h*2.0/4]
        self.p0[5][0] = [x+w*2.0/4,y+h*3.0/4]
        self.p0[6][0] = [x+w*3.0/4,y+h*1.0/4]
        self.p0[7][0] = [x+w*3.0/4,y+h*2.0/4]
        self.p0[8][0] = [x+w*3.0/4,y+h*3.0/4]

        self.center = util.Point(int(x+w/2), int(y+h/2))
        self.radius = math.sqrt(w**2 + h**2)
        self.nump0 = self.p0.shape[0]
    
    def process(self, src, **kwargs):
        sw = util.SW('Optical Flow')
        
        frame_gray = cv2.cvtColor(src, cv2.COLOR_BGR2GRAY)
        p0 = self.p0

        # calculate optical flow
        p1, st, err = cv2.calcOpticalFlowPyrLK(self.old_gray, frame_gray, p0, None, 
                                               winSize  = (15,15),
                                               maxLevel = 2,
                                               criteria = (cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT, 10, 0.03))
        
        # Select good points
        good_new = p1[st==1]
        good_old = p0[st==1]
        rstmsk = np.zeros(good_new.shape[0], dtype=np.bool8)

        for i,pt in enumerate(good_new):
            rstmsk[i] = np.bool8(math.sqrt((pt[0]-self.center.x)**2+(pt[1]-self.center.y)**2)<=(self.radius+SELECTPADDING))
        
        good_new = good_new[rstmsk]
        good_old = good_old[rstmsk]
        
        if (good_new.shape[0]*2)<self.nump0:
            raise OpticalFlow.ObjectMissError
        
        tmp = np.average(good_new, axis=0)
        self.center = util.Point(int(tmp[0]),int(tmp[1]))
        
        dst = src.copy()
        
        try:
            self.oflines # 光流轨迹线
        except AttributeError:
            self.oflines = np.zeros_like(src, dtype=np.uint8)
        
        for n,o in zip(good_new, good_old):
            cv2.circle(dst,tuple(n),7,OBJECT_MATCH_COLOR,-1)# filled circle
            cv2.line(self.oflines,tuple(n),tuple(o),OBJECT_MATCH_COLOR,7)# filled circle
        self.old_gray = frame_gray
        self.p0 = good_new.reshape(-1,1,2)
        
        sw.stop()
        return dst, [self.center], cv2.add(self.oflines,src)

# ---- 目标跟踪类 ----
class ObjectTrack(object):
    def __init__(self, rect, src, hist_channel = [0]):
        lt = rect[0]
        rb = rect[1]
        self.track_window = (lt.x, lt.y, rb.x-lt.x, rb.y-lt.y)
        roi = src[ lt.y:rb.y , lt.x:rb.x ,:].copy()
        
        self.tplmatch = TemplateMatch(src, roi)
        self.meanshift = MeanShift(src, roi, self.track_window, hist_channel)
        self.graymeanshift = GrayMeanShift(src, roi, self.track_window)
        self.opticalflow = OpticalFlow(src, self.track_window)
        
        self.methods = {METHOD.TEMPLATEMATCH:   self.tplmatch,
                        METHOD.MEANSHIFT:       self.meanshift,
                        METHOD.GRAYMEANSHIFT:   self.graymeanshift,
                        METHOD.OPTICALFLOW:     self.opticalflow,
                        }
    
    def process(self, method, src, **kwargs):
        try:
            rst, center, res = self.methods[method].process(src, **kwargs)
        except OpticalFlow.ObjectMissError:
            # @FIXME:在光流中加入判断，有效点个数过少则重新标定
            #self.opticalflow.reinit(src, kwargs['center'])
            center = None
        
        if center:
            return rst,center,res
        else:# 目标丢失
            return src, None, src
    
    @staticmethod
    def draw_circles(src, center, color=None, radius=20):
        if color is None:
            color = OBJECT_MATCH_COLOR
        else:
            color = (0, 255,0)
        dst = src.copy()
        if isinstance(center, list) or isinstance(center, tuple):
            for c in center:
                assert isinstance(c, util.Point), 'points in center must be util.Point'
                cv2.circle(dst, c.tup, radius, color, LINE_WIDTH)
        else:
            assert isinstance(center, util.Point), 'center must be util.Point'
            cv2.circle(dst, center.tup, radius, color, LINE_WIDTH)
        
        return dst
    
    