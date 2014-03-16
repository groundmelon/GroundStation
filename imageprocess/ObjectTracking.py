# -*- coding: utf-8 -*- 
'''
Created on 2014-2-13

@author: GroundMelon
'''
import cv2
import numpy as np
import util

LINE_WIDTH = 5
DRAG_COLOR = (255,0,0)
OBJECT_MATCH_COLOR = (0, 0, 255)
HUE_DELTA = 30
SAT_DELTA = 30
VAL_DELTA = 30
MEDIANBLUR_KERNEL_SIZE = 5

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
    @bitmap_size:显示区域的尺寸
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
    @bitmap_size:显示区域的尺寸
    @return: 画框的图像
    '''
    width = src_size[1]
    height = src_size[0]
    bw = bitmap_size[0] # bitmap width
    bh = bitmap_size[1] # bitmap height
    
    start = util.Point(drag_data['start'].x * width / bw, drag_data['start'].y * height / bh)
    end = util.Point(drag_data['end'].x * width / bw, drag_data['end'].y * height / bh)
    left_top = util.Point(min(start.x, end.x), min(start.y, end.y))
    right_bottom = util.Point(max(start.x, end.x), max(start.y, end.y))
    return (left_top, right_bottom)

# ---- 目标匹配相关 ----
class ObjectMatch(object):
    def __init__(self, rect, src):
        lt = rect[0]
        rb = rect[1]
        self.object_template =  src[ lt.y:rb.y , lt.x:rb.x ,:]
        rtn = self.calc_color_match_value(self.object_template)
        hue = rtn['h']
        sat = rtn['s']
        val = rtn['v']
        sat_lower = max(0, sat-SAT_DELTA)
        sat_upper = min(255, sat+SAT_DELTA)
        val_lower = max(0, val-VAL_DELTA)
        val_upper = min(255, val+VAL_DELTA)
        self.threshold=[]
        if 0 < hue <= HUE_DELTA:
            self.threshold.append(np.array([0,                 sat_lower, val_lower]))
            self.threshold.append(np.array([hue+HUE_DELTA,     sat_upper, val_upper]))
            self.threshold.append(np.array([hue-HUE_DELTA+180, sat_lower, val_lower]))
            self.threshold.append(np.array([180,               sat_upper, val_upper]))
        elif (180-HUE_DELTA) < hue < HUE_DELTA:
            self.threshold.append(np.array([hue-HUE_DELTA,     sat_lower, val_lower]))
            self.threshold.append(np.array([180,               sat_upper, val_upper]))
            self.threshold.append(np.array([0,                 sat_lower, val_lower]))
            self.threshold.append(np.array([hue+HUE_DELTA-180, sat_upper, val_upper])) 
        else: #正常情况
            self.threshold.append(np.array([hue-HUE_DELTA, sat_lower, val_lower]))
            self.threshold.append(np.array([hue,           sat_upper, val_upper]))
            self.threshold.append(np.array([hue,           sat_lower, val_lower]))
            self.threshold.append(np.array([hue+HUE_DELTA, sat_upper, val_upper])) 
        self.selected_hsv = rtn                         
        self.center = util.Point((lt.x+rb.x)/2, (lt.y+rb.y)/2)
        self.radius = int((((rb.y-lt.y)**2 + (rb.x-lt.x)**2)**0.5)/2)
        
        #---- 测试各种方法是否有效 ----
        self.do_match(src)
        self.do_color_match(src)
        
    def calc_color_match_value(self, selected_img):    
        bgr = selected_img.copy()
        hsv = cv2.cvtColor(bgr, cv2.COLOR_BGR2HSV)
        h,s,v = cv2.split(hsv)
        selected = {}
        selected['h'] = int(np.median(h))
        selected['s'] = int(np.median(s))
        selected['v'] = int(np.median(v))
        
        print('selected color is %s'%str(selected))
        return selected 
    
    def do_match(self, src):
        methods = ['cv2.TM_CCOEFF', 'cv2.TM_CCOEFF_NORMED', 'cv2.TM_CCORR',
            'cv2.TM_CCORR_NORMED', 'cv2.TM_SQDIFF', 'cv2.TM_SQDIFF_NORMED']
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
        
        rst_img = src.copy()
        cv2.rectangle(rst_img,tl, br, OBJECT_MATCH_COLOR, LINE_WIDTH)
#        return (rst_img, util.Point(tl), util.Point(br))
        return (rst_img, util.Point((tl[0]+br[0])/2, (tl[1]+br[1])/2))
    
    def do_color_match(self, src):
        hsv = cv2.cvtColor(src, cv2.COLOR_BGR2HSV)
        mask1 = cv2.inRange(hsv, self.threshold[0], self.threshold[1])
        mask2 = cv2.inRange(hsv, self.threshold[2], self.threshold[3])
        mask = cv2.bitwise_or(mask1, mask2)
        filted_mask = cv2.medianBlur(mask, int(self.radius/2) + (self.radius/2)%2 - 1)
        rtn = cv2.moments(filted_mask)
        m10 = rtn['m10']
        m01 = rtn['m01']
        m00 = rtn['m00']
        assert m00 != 0, u'没有可匹配的目标'
        rst_img = src.copy()
        center = (int(m10/m00), int(m01/m00))
        cv2.circle(rst_img, center, self.radius, OBJECT_MATCH_COLOR, LINE_WIDTH)
        msk_img = cv2.cvtColor(filted_mask, cv2.COLOR_GRAY2BGR)
        return (rst_img, util.Point(center), msk_img)
        
        