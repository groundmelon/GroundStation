# -*- coding: utf-8 -*- 
'''
Created on 2014-4-1

@author: GroundMelon
'''
from util import Point as Pt
import math

BUFFERSIZE = 100
PADDING_SCALE = 0.25
PT_PITCH_in_rad = 45.0/180 * math.pi

class PID():
    def __init__(self, p, i, d):
        self.Kp = p
        self.Ki = i
        self.Kd = d
X = PID(4.4,13,0)
Y = PID(4.4,13,0)
Z = PID(1,0,0)

class TrackController():
    def __init__(self, image_size, sample_time):
        self.ts = sample_time
        self.pts = []
        self.w = image_size[0]
        self.h = image_size[1]
        self.spdmax = self.dtc(Pt(0,0), Pt(self.w, self.h))
        self.midpt = Pt(self.w*0.5, self.h*0.5)
        
    def dtc(self, p, q):
        '''Calculate distance of two points'''
        assert isinstance(p, Pt)
        assert isinstance(q, Pt)
        return math.sqrt((p.x-q.x)**2 + (p.y-q.y)**2)
    
    def update_h(self, height):
        self.dis = height / math.sin(PT_PITCH_in_rad)
        self.height = height
    
#     def add_pt(self, center):
#         assert isinstance(center, (list, tuple))
#         if len(self.pts) < 2 and len(center)==1:
#             self.pts.append(center[0])
#             return
#         
#         wait_list = []
#         # 选择中间部分
#         for c in center:
#             if self.w * PADDING_SCALE < c.x < self.w * (1 - PADDING_SCALE) and \
#             self.h * PADDING_SCALE < c.y < self.h * (1 - PADDING_SCALE):
#                 wait_list.append(c)
#                 
#         # 筛选速度变化符合要求的点
#         for c in wait_list:
#             if self.dtc(c, self.pts[-1]) > self.spdmax:
#                 wait_list.remove(c)
#         
#         # 选择距离最近的点
#         nearest_pt = Pt(0,0)
#         for c in wait_list:
#             if self.dtc(nearest_pt, self.midpt) > self.dtc(c, self.midpt):
#                 nearest_pt = c
#         
#         if nearest_pt.x and nearest_pt.y:
#             self.pts.append(nearest_pt)
#         else:
#             print('No valid point')
#         
#         if len(self.pts)>BUFFERSIZE:
#             self.pts.pop(0)
    
    def add_pt(self, center):
        assert isinstance(center, (list, tuple))
        if len(self.pts) < 2 and len(center)==1:
            self.pts.append(center[0])
            return
        
        c = center[0] # 历史遗留问题，目前center内只有1个点，故按照该点处理
        # 选择中间部分
        if self.w * PADDING_SCALE < c.x < self.w * (1 - PADDING_SCALE) and \
        self.h * PADDING_SCALE < c.y < self.h * (1 - PADDING_SCALE) and \
        self.dtc(c, self.pts[-1]) > self.spdmax:# 筛选速度变化符合要求的点
            p = Pt()
            try:# alpha滤波
                self.pts[-1] = self.pts[-1]*ALPHA + self.pts[-2]*(1-ALPHA)
            except IndexError:# 个数不够无法滤波
                pass
        
        if len(self.pts)>BUFFERSIZE:
            self.pts.pop(0)
    def get_u(self):
        assert len(self.pts)>=1
        dy = self.w * 0.5 - self.pts[-1].x
        dx = self.h * 0.5 - self.pts[-1].y
        # x-y in camera is not x-y-z in UAV
        
        ex, ey = self.pixel_to_real(dx, dy, self.dis)
        ez = 180.0/math.pi * math.atan2(float(ey), (self.height/float(math.tan(PT_PITCH_in_rad))))
        
        if len(self.pts)>=2:
            ey0, ex0 = self.pixel_to_real(self.w * 0.5 - self.pts[-2].x, 
                                          self.h * 0.5 - self.pts[-2].y, 
                                          self.dis)
            ez0 = math.atan2(float(ey0), (self.height/float(math.tan(PT_PITCH_in_rad))))
            du = (X.Kp * (ex-ex0) + X.Ki * (ex), 
                  0,                            #Y.Kp * (ey-ey0) + Y.Ki * (ey), 
                  Z.Kp * (ez-ez0) + Z.Ki * (ez)
                  )
        else:
            du = (X.Kp * ex, 0, Z.Kp * ez)
        print('du<X=%.2f,Y=%.2f,Z=%.2f>'%du)
        return du
    
    def pixel_to_real(self, w, h, distance):
        real_w = 1.6115 * distance * w / self.w
        real_h = 1.2450 * distance * h / self.h
        return (real_w, real_h)

if __name__ == '__main__':
    ctrl = TrackController((100,100))
    ctrl.update_h(1)
    ctrl.add_pt([Pt(50,50)])
    ctrl.add_pt([Pt(50,50)])
    while True:
        s = raw_input('Input centers:')
        c = []
        for item in s.split(' '):
            c.append(eval('Pt%s'%item))
        ctrl.add_pt(c)
        ctrl.get_u()
        #print(ctrl.pts)