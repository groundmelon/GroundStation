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
HUE_DELTA = 30
SAT_DELTA = 30
LIG_DELTA = 30
MEDIANBLUR_KERNEL_SIZE = 5

MULTI_SPLIT_SCALE = 0.2

CANNY_MIN = 100
CANNY_MAX = 200


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

# ---- 目标匹配相关 ----
class ObjectMatchMultiProcess(object):
    def __init__(self, rect, src, hist_channel = [0]):
        lt = rect[0]
        rb = rect[1]
        self.track_window = (lt.x, lt.y, rb.x-lt.x, rb.y-lt.y)
        self.track_window_origin = self.track_window
        roi = src[ lt.y:rb.y , lt.x:rb.x ,:].copy()
        self.hist_channel = hist_channel
        # ---- preparation for template match ----
        self.object_template =  roi
         
        # ---- preparation for edge template match ----
        self.edge_tpl = cv2.Canny(roi, CANNY_MIN, CANNY_MAX)
        
        # ---- preparation for color match ----
#         rtn = self.calc_color_match_value(roi)
#         hue = rtn['h']
#         sat = rtn['s']
#         lig = rtn['l']
#         sat_lower = max(0, sat-SAT_DELTA)
#         sat_upper = min(255, sat+SAT_DELTA)
#         lig_lower = max(0, lig-LIG_DELTA)
#         lig_upper = min(255, lig+LIG_DELTA)
#         self.threshold=[]
#         if 0 < hue <= HUE_DELTA:
#             self.threshold.append(np.array([0,                 sat_lower, lig_lower]))
#             self.threshold.append(np.array([hue+HUE_DELTA,     sat_upper, lig_upper]))
#             self.threshold.append(np.array([hue-HUE_DELTA+180, sat_lower, lig_lower]))
#             self.threshold.append(np.array([180,               sat_upper, lig_upper]))
#         elif (180-HUE_DELTA) < hue < HUE_DELTA:
#             self.threshold.append(np.array([hue-HUE_DELTA,     sat_lower, lig_lower]))
#             self.threshold.append(np.array([180,               sat_upper, lig_upper]))
#             self .threshold.append(np.array([0,                 sat_lower, lig_lower]))
#             self.threshold.append(np.array([hue+HUE_DELTA-180, sat_upper, lig_upper])) 
#         else: #正常情况
#             self.threshold.append(np.array([hue-HUE_DELTA, sat_lower, lig_lower]))
#             self.threshold.append(np.array([hue,           sat_upper, lig_upper]))
#             self.threshold.append(np.array([hue,           sat_lower, lig_lower]))
#             self.threshold.append(np.array([hue+HUE_DELTA, sat_upper, lig_upper])) 
        #self.selected_hls = rtn                         
        self.center = util.Point((lt.x+rb.x)/2, (lt.y+rb.y)/2)
        self.radius = int((((rb.y-lt.y)**2 + (rb.x-lt.x)**2)**0.5)/2)
        
        # ---- preparation for meanshift ----
        hls_roi = cv2.cvtColor(roi, cv2.COLOR_BGR2HLS)
        #mask = cv2.inRange(hls_roi, np.array((0., 60., 32.)), np.array((180.,255.,255.)))
        mask = cv2.inRange(hls_roi, np.array((0., 0., 0.)), np.array((180.,255.,255.)))
        self.roi_hist = cv2.calcHist([hls_roi], self.hist_channel, mask, [180], [0,180])
        cv2.normalize(self.roi_hist, self.roi_hist, 0, 255, cv2.NORM_MINMAX)
        
        self.term_crit = (cv2.TERM_CRITERIA_EPS|cv2.TERM_CRITERIA_COUNT, 10, 1)
        
        # ---- preparation for multi-meanShift ----
        #self.d2_th = (src.shape[1]**2 + src.shape[0]**2) * (MULTI_SPLIT_SCALE**2) 
        self.d2_th = self.radius ** 2

        # ---- preparation for gray-meanShift ----
        gray_roi = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)
#         mask = cv2.inRange(gray_roi, np.array((0.)), np.array((255.)))
        self.roi_gray_hist = cv2.calcHist([gray_roi], [0], None, [255], [0,255])
        cv2.normalize(self.roi_gray_hist, self.roi_gray_hist, 0, 255, cv2.NORM_MINMAX)
                
        # ---- preparation for optical flow ----
        feature_params = dict( maxCorners = 100,
                       qualityLevel = 0.3,
                       minDistance = 10,
                       blockSize = 7 )
        self.old_gray = cv2.cvtColor(src, cv2.COLOR_BGR2GRAY)
        self.opmask = np.zeros_like(self.old_gray, np.uint8)
        self.opmask[(lt.y-SELECTPADDING):(rb.y+SELECTPADDING), (lt.x-SELECTPADDING):(rb.x+SELECTPADDING)]=255
        self.p0 = cv2.goodFeaturesToTrack(self.old_gray, mask = self.opmask, **feature_params)
        self.ofc = self.center
        
        #---- 测试各种方法是否有效 ----
        self.do_tpl_match(src)
        #self.do_color_match(src)
        self.edge_match_maxval = self.do_edge_match(src, test=True)
        
#     def calc_color_match_value(self, selected_img):    
#         bgr = selected_img.copy()
#         hls = cv2.cvtColor(bgr, cv2.COLOR_BGR2HLS)
#         h,l,s = cv2.split(hls)
#         selected = {}
#         selected['h'] = int(np.median(h))
#         selected['l'] = int(np.median(l))
#         selected['s'] = int(np.median(s))
#         
#         print('selected color is %s'%str(selected))
#         return selected 
    
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
    
    def remove_near_points(self, pts):
        rst = []
        for p in pts:
            assert isinstance(p, util.Point), 'p in pts must be util.Point'
            if not rst:
                rst.append(p)
            else:
                dumplicate = False
                for r in rst:
                    d2 = (p.x - r.x) ** 2 + (p.y - r.y) ** 2
                    if d2 < self.d2_th:
                        dumplicate = True
                if not dumplicate:
                    rst.append(p)
        return rst
    
    def pick_near_points(self, pts0, pts1):
        rst = []
        for p0 in pts0:
            for p1 in pts1:
                d2 = (p0.x - p1.x)**2 + (p0.y - p1.y)**2
                if d2 < self.d2_th:
                    rst.append(p0)
        #print '%d & %d -> %s'%(len(pts0),len(pts1),str(rst)),
        return rst
    
    def do_optical_flow(self, src, **kargs):
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
            rstmsk[i] = np.bool8(math.sqrt((pt[0]-self.ofc.x)**2+(pt[1]-self.ofc.y)**2)<=(self.radius+SELECTPADDING))
        
        tmp = good_new[rstmsk]
        good_new = tmp
        tmp = good_old[rstmsk]
        good_old = tmp
        
        tmp = np.average(good_new, axis=0)
        self.ofc = util.Point(int(tmp[0]),int(tmp[1]))
        
        dst = src.copy()
        try:
            self.oflines
        except AttributeError:
            self.oflines = np.zeros_like(src, dtype=np.uint8)
        
        for n,o in zip(good_new, good_old):
            cv2.circle(dst,tuple(n),5,OBJECT_MATCH_COLOR,-1)# filled circle
            cv2.line(self.oflines,tuple(n),tuple(o),OBJECT_MATCH_COLOR,2)# filled circle
        self.old_gray = frame_gray
        self.p0 = good_new.reshape(-1,1,2)
        
        return dst, [self.ofc], cv2.add(self.oflines,src)
    
    def do_tpl_match(self, src, **kargs):
#         sw = util.SW('tpl-match')
        
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
        
#         sw. stop()
        return (rst_img, [util.Point(center)], rst_res)
    
    def do_edge_match(self, src, test=False, **kargs):
#         sw = util.SW('edge-tpl-match')
        
        # ---- 参数处理 -----
        if kargs.get('arg'):
            match_scale = kargs['arg']
        else:
            match_scale = 0.1
        
        src_edge = cv2.Canny(src, 100,200)
        
        methods = ['cv2.TM_CCOEFF', 'cv2.TM_CCOEFF_NORMED', 'cv2.TM_CCORR',
            'cv2.TM_CCORR_NORMED', 'cv2.TM_SQDIFF', 'cv2.TM_SQDIFF_NORMED']
        method = eval(methods[0])
        res = cv2.matchTemplate(src_edge, self.edge_tpl, method)
        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)
        
        if not test:
            if max_val < (self.edge_match_maxval * match_scale):
                null_img = np.zeros_like(src)
                return (null_img, util.Point((0,0)), null_img)
        
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
        rst_edge = cv2.cvtColor(src_edge, cv2.COLOR_GRAY2BGR)
        cv2.rectangle(rst_edge,tl, br, OBJECT_MATCH_COLOR, LINE_WIDTH)
        cv2.putText(rst_edge,'%.2f'%max_val, (0,rst_edge.shape[0]), cv2.FONT_HERSHEY_SIMPLEX, 2, OBJECT_MATCH_COLOR, LINE_WIDTH)
        
#         sw.stop()
        if test:
            return max_val
        else:
            return (rst_img, [center], rst_edge)
        
    def do_multi_edge_match(self, src, **kargs):
#         sw = util.SW('multi-edge-tpl-match')
        
        # ---- 参数处理 -----
        assert kargs.has_key('arg'), 'No arg naming "arg"'
        if kargs.get('arg'):
            match_scale = kargs['arg']
        else:
            match_scale = 0.95
        
        src_edge = cv2.Canny(src, 100,200)
        
        methods = ['cv2.TM_CCOEFF', 'cv2.TM_CCOEFF_NORMED', 'cv2.TM_CCORR',
            'cv2.TM_CCORR_NORMED', 'cv2.TM_SQDIFF', 'cv2.TM_SQDIFF_NORMED']
        if match_scale > 1:
            method = eval(methods[4])
        else:
            method = eval(methods[0])
        #sw.pause()
        res = cv2.matchTemplate(src_edge, self.edge_tpl, method)
        #sw.pause()
        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)
        if match_scale > 1:
            msk = np.less(res, min_val * match_scale)
        else:
            msk = np.greater(res, max_val * match_scale)
        indice = np.nonzero(msk)
        pts = [util.Point(indice[1][i],indice[0][i]) for i in range(indice[0].shape[0])]
        dots = self.remove_near_points(pts)
        w = self.track_window[2]
        h = self.track_window[3]
        center = [util.Point(d.x+w/2, d.y+h/2) for d in dots]      
        
#         sw.stop()
        return (None, center, None)
    
    def do_color_match(self, src, **kargs):
#         sw = util.SW('color-match')

#         hls = cv2.cvtColor(src, cv2.COLOR_BGR2HLS)
#         mask1 = cv2.inRange(hls, self.threshold[0], self.threshold[1])
#          mask2 = cv2.inRange(hls, self.threshold[2], self.threshold[3])
#         mask = cv2.bitwise_or(mask1, mask2)
#         filted_mask = cv2.medianBlur(mask, int(self.radius/2) + (self.radius/2)%2 - 1)
#         rtn = cv2.moments(filted_mask)
#         m10 = rtn['m10']
#         m01 = rtn['m01']
#         m00 = rtn['m00']
#         assert m00 != 0, u'没有可匹配的目标'
#         rst_img = src.copy()
#         center = (int(m10/m00), int(m01/m00))
#         cv2.circle(rst_img, center, self.radius, OBJECT_MATCH_COLOR, LINE_WIDTH)
#         msk_img = cv2.cvtColor(filted_mask, cv2.COLOR_GRAY2BGR)
        
#         sw.stop()
        rst_img = src[::-1,:,:]
        msk_img = src[:,::-1,:]
        center = (0,0)
        
        return (rst_img, [util.Point(center)], msk_img)

    def do_meanshift(self, src, **kargs):         
#         sw = util.SW('meanShift')
         
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
        
#         sw.stop()
        return rst_img, [util.Point(center)], prj_img
    
    def do_gray_meanshift(self, src,**kargs):
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
    
    def do_multi_meanshift(self, src, **kargs):
        
        # ---- 参数处理 -----
        assert kargs.has_key('arg'), 'No arg naming "arg"'
        if kargs.get('arg'):
            effect_value_multiplier = kargs['arg']
        else: 
            effect_value_multiplier = 3 
        
#         sw = util.SW('multi-meanShift')
        
        hls = cv2.cvtColor(src, cv2.COLOR_BGR2HLS)
        dst = cv2.calcBackProject([hls], self.hist_channel, self.roi_hist, [0,180], 1)
        win_w = self.track_window_origin[2]
        win_h = self.track_window_origin[3]
        
        search_unit_x = win_w 
        search_unit_y = win_h 
        hist_record=[]
        for i in range((src.shape[1]-win_w)/search_unit_x):
            for j in range((src.shape[0]-win_h)/search_unit_y):        
                x,y = i*search_unit_x, j*search_unit_y 
                hist = cv2.calcHist([dst[y : y+win_h, x : x+win_w]],[0],None,[8],[0,256])
                #print('(%3d,%3d)%s'%(x,y,str(['%5.0f'%x[0] for x in hist.tolist()])))
                hist_record.append((x,y,hist.tolist()[0][0]))
        #print('\n'.join([str(x) for x in hist_record]))
        
        data = np.array(hist_record, dtype=np.int)
        max_index = np.argmax(data, axis=0)[2]
        min_index = np.argmin(data, axis=0)[2]
        thershold = int((hist_record[max_index][2] - hist_record[min_index][2]) / effect_value_multiplier
                        + hist_record[min_index][2])
        msk = np.less(data[:,2],thershold)
        valid = data[msk].tolist()
        #print('th=%d msk=%s va=%s'%(thershold,str(msk),str(valid_hist_info)))
        center_list=[]
        for i in range(len(valid)):
            track_window = (valid[i][0], valid[i][1], win_w, win_h)
            ret, window = cv2.meanShift(dst, track_window, self.term_crit)
            center = util.Point(int(window[0]+window[2]/2), int(window[1]+window[3]/2))
            center_list.append(center)
            center_list = self.remove_near_points(center_list)
            
        rst_img = src.copy()
        for c in center_list:
            cv2.circle(rst_img, c.tup, 40, OBJECT_MATCH_COLOR, LINE_WIDTH)
        
        prj_img = cv2.cvtColor(dst, cv2.COLOR_GRAY2BGR)
        
#         sw.stop()
        return rst_img, center_list, prj_img
    
    def do_mix(self, src, **kargs):
#         sw = util.SW('mix')
        
        # ---- 参数处理 -----
        assert kargs.has_key('multimean_arg')
        assert kargs.has_key('edgetpl_arg')
        multimean_arg = kargs.get('multimean_arg')
        edgetpl_arg = kargs.get('edgetpl_arg')
        
        _, pts0, _ = self.do_multi_meanshift(src, {'arg':multimean_arg})
        _, pts1, _ = self.do_multi_edge_match(src, {'arg':edgetpl_arg})
        pts = self.pick_near_points(pts0, pts1)
        dst = self.draw_circles(src, pts)
        
#         sw.stop()
        return dst, pts, dst

def child_process(lock, fa2ch, ch2fa, objmatch):
    '''目标匹配子进程的执行函数
    
    '''
    with lock:
        print('Child PID %s Start'%os.getpid())
        sys.stdout.flush()
    
    while True:
        try:
            rst = None
            args = fa2ch.get(block=True, timeout=5)
            # objmatch.do_***_match(src=args[1], **kargs=args[2])
            with lock:
                if args[0] == 'do_tpl_match':
                    rst = objmatch.do_tpl_match(args[1], **args[2])
                elif args[0] == 'do_edge_match':
                    rst = objmatch.do_edge_match(args[1], **args[2])
                elif args[0] == 'do_meanshift':
                    rst = objmatch.do_meanshift(args[1], **args[2])
                elif args[0] == 'do_multi_meanshift':
                    rst = objmatch.do_multi_meanshift(args[1], **args[2])
                elif args[0] == 'do_gray_meanshift':
                    rst = objmatch.do_gray_meanshift(args[1], **args[2])
                elif args[0] == 'do_mix':
                    rst = objmatch.do_mix(args[1], **args[2])
                elif args[0] == 'do_optical_flow':
                    rst = objmatch.do_optical_flow(args[1], **args[2])
                else:
                    assert False, 'invalid match type!'
        except QEmpty:
            break;# timeout, main process is terminated, exit loop
        try:
            if rst:
                ch2fa.put(rst,block=True, timeout=5)
        except QFull:
            break;# timeout, main process is terminated, exit loop
    
    ch2fa.cancel_join_thread()
    with lock:
        print('Child PID %s Timeout Exit...'%os.getpid())
        sys.stdout.flush()

    return

class ObjectMatch(object):        
    def __init__(self, rect, src, hist_channel = [0]):
        self.objmatch = ObjectMatchMultiProcess(rect, src, hist_channel)
        self.last_rst = (src, 
                         [util.Point((rect[0].x+rect[1].x)/2,(rect[0].y+rect[1].y)/2)],
                         src)
        self.lock = multiprocessing.Lock()
        self.fa2ch = JoinableQueue(1)
        self.ch2fa = JoinableQueue(1)
        with self.lock:
            print('server PID %s'%os.getpid())
            sys.stdout.flush()
        child_proc = Process(target=child_process, args=(self.lock, self.fa2ch, self.ch2fa, self.objmatch))
        child_proc.start()
        
        
    
    def draw_circles(self, src, center, color=None, radius=20):
        return self.objmatch.draw_circles(src, center, color, radius)
    
    def do_match(self, methodstr, src, **kargs):
        try:
            self.fa2ch.put((methodstr,src,kargs), block=False)
        except QFull:
            pass
        rst = None
        try:    
            rst = self.ch2fa.get(block=False, timeout=0)
        except QEmpty:
            pass
        if rst is not None:
            self.last_rst = rst
        return self.last_rst
    
    def do_tpl_match(self, src, **kargs):
        return self.do_match('do_tpl_match', src, **kargs)
    
    def do_edge_match(self, src, **kargs):
        return self.do_match('do_edge_match', src, **kargs)
    
    def do_meanshift(self, src, **kargs):
        return self.do_match('do_meanshift', src, **kargs)
    
    def do_multi_meanshift(self, src, **kargs):
        return self.do_match('do_multi_meanshift', src, **kargs)
    
    def do_gray_meanshift(self, src, **kargs):
        return self.do_match('do_gray_meanshift', src, **kargs)
    
    def do_mix(self, src, **kargs):
        return self.do_match('do_mix', src, **kargs)
    
    def do_optical_flow(self, src, **kargs):
        return self.do_match('do_optical_flow', src, **kargs)
    
    
        