# -*- coding: utf-8 -*- 
'''
Created on 2014-4-1

@author: GroundMelon
'''
import util
import math

BUFFERSIZE = 100
PADDING_SCALE = 0.10
PT_PITCH_in_rad = 45.0/180 * math.pi

def get_alpha(n):
    return 1-(0.1)**(1.0/n)

def thlimit(x,a,b):
    assert a<b
    if x < a:
        return a
    elif x > b:
        return b
    else:
        return x

def sign(x):
    if x > 0:
        rtn = 1
    elif x == 0:
        rtn = 0
    else:
        rtn = -1
    return rtn

class PID():
    def __init__(self, p, i, d):
        self.Kp = p
        self.Ki = i
        self.Kd = d
X = PID(0,0,0)
Y = PID(-5,0,-0)
Z = PID(0.4,0,0)

class Pt(util.Point,object):
    def __init__(self, *args):
        try:
            super(Pt, self).__init__(*args)
        except AssertionError,e:
            if e.args[0]=='arg is not tuple':
                super(Pt, self).__init__(tuple(args[0]))
        self.used=False
    

class TrackController():
    def __init__(self, image_size, sample_time):
        self.ts = sample_time
        self.pts = []
        self.w = image_size[0]
        self.h = image_size[1]
        self.spdmax = self.dtc(Pt(0,0), Pt(self.w, self.h))
        self.midpt = Pt(self.w*0.5, self.h*0.5)
        self.alpha = get_alpha(4)
        
        # TODO: UAV未开启追踪，地面站已开启，积分问题
#         self.integral=dict(pitch=0,yaw=0,roll=0) 
        
    def dtc(self, p, q):
        '''Calculate distance of two points'''
        assert isinstance(p, Pt)
        assert isinstance(q, Pt)
        return math.sqrt((p.x-q.x)**2 + (p.y-q.y)**2)
    
    def update_h(self, height):
        self.dis = height / math.sin(PT_PITCH_in_rad)
        self.height = height
    
    def add_pt(self, center):
        assert isinstance(center, (list, tuple))
        if len(self.pts) < 2:
            c = center[0] # 历史遗留问题，目前center内只有1个点，故按照该点处理
            assert isinstance(c, util.Point)
            self.pts.append(Pt(c))
            return
        
        c = Pt(center[0]) # 历史遗留问题，目前center内只有1个点，故按照该点处理
        # 选择中间部分
        if self.w * PADDING_SCALE < c.x < self.w * (1 - PADDING_SCALE) and \
        self.h * PADDING_SCALE < c.y < self.h * (1 - PADDING_SCALE) and \
        self.dtc(c, self.pts[-1]) < self.spdmax:# 筛选速度变化符合要求的点
            try:# alpha滤波
                p=Pt()
                p.x = int((1-self.alpha) * self.pts[-1].x + self.alpha * c.x)
                p.y = int((1-self.alpha) * self.pts[-1].y + self.alpha * c.y)
                assert isinstance(c, Pt)
                self.pts.append(p)
            except IndexError:# 个数不够无法滤波
                pass
        else:
            print("Invalid Point")
        
        if len(self.pts)>BUFFERSIZE:
            self.pts.pop(0)
    def get_u(self,nt,pt_pitch):
        global PT_PITCH_in_rad
        PT_PITCH_in_rad = -pt_pitch/180.0 * math.pi
        print PT_PITCH_in_rad
        # --- 前几个点，做一些初始化工作 ---
        if len(self.pts)<=2:
            self.last_time = nt
            return (0,0,0)
        
        # --- 更新时间间隔 ---
#         dt = nt-self.last_time
#         self.last_time = nt
        
        # --- 没有新的有效点出现，返回0控制量 ---
        if self.pts[-1].used:
#             assert False, 'No new point' 
            return (0,0,0)
        self.pts[-1].used = True
        
        # --- 计算像素距离 ---
        dx_camera = self.w * 0.5 - self.pts[-1].x
        dy_camera = self.h * 0.5 - self.pts[-1].y
        # x-y in camera --> y-x in UAV
        
        
        # --- 计算实际距离 ---
        ex, ey = self.pixel_to_real(dy_camera, dx_camera, self.dis)
        ez = 180.0/math.pi * math.atan2(float(ey), (self.height/float(math.tan(PT_PITCH_in_rad))))
        
        
        # 计算上次偏差
        ey0, ex0 = self.pixel_to_real(self.w * 0.5 - self.pts[-2].x, 
                                      self.h * 0.5 - self.pts[-2].y, 
                                      self.dis)
        ez0 = math.atan2(float(ey0), (self.height/float(math.tan(PT_PITCH_in_rad))))
        
        # 计算上上次偏差
        ey00, ex00 = self.pixel_to_real(self.w * 0.5 - self.pts[-3].x, 
                                      self.h * 0.5 - self.pts[-3].y, 
                                      self.dis)
        ez00 = math.atan2(float(ey00), (self.height/float(math.tan(PT_PITCH_in_rad))))
        
        # --- PITCH轴控制方法 ---
#         u_pitch = Y.Kp * (ex-ex0) + Y.Ki * (ex) + Y.Kd * ((ex-ex0)-(ex0-ex00)),# 增量式PID 
#         u_pitch = Y.Kp * ex # 绝对式P控制
        u_pitch = abs(ex)**1 * 2 * sign(ex)  # 变增益P控制
        
        # --- YAW轴控制方法 ---
        u_yaw = Z.Kp * (ez-ez0) + Z.Ki * (ez) # 增量式PID   
        
        
        # --- 输出限制 ---
        u_pitch = thlimit(u_pitch,-3,3)
        u_yaw = thlimit(u_yaw, -30, 30)
        
#         # pitch轴位置环和速度环
#         # Kp_pitch_pos = 1
#         Kp_pitch_speed = 1
#         #v = ex * Kp_pitch_pos
#         v = abs(ex)**1.5
#         u_pitch = (v-flowspeedx) * Kp_pitch_speed
#         u_pitch = thlimit(u_pitch,-2.0,2.0) 
#         
#         # roll轴位置环和速度环
#         # 不进行位置控制 Kp_roll_pos = 0
#         Kp_roll_speed = 1
#         v=0 # 不进行位置控制 v = ex * Kp_roll_pos
#         u_roll = (v-flowspeedy) * Kp_roll_speed
#         u_roll = thlimit(u_roll,-2.0,2.0) 
        
        #
        du = (0,
              u_pitch,
              u_yaw
              )
        return du
    
    def pixel_to_real(self, w, h, distance):
        real_w = 1.6115 * distance * w / self.w
        real_h = 1.2450 * distance * h / self.h
        return (real_w, real_h)

if __name__ == '__main__':
    ctrl = TrackController((100,100),0.1)
    ctrl.update_h(1)
    while True:
        s = raw_input('Input centers:')
        c = []
        for item in s.split(' '):
            c.append(eval('Pt%s'%item))
        ctrl.add_pt(c)
        print ('du<%.2f,%.2f,%.2f>'%ctrl.get_u())
        print(ctrl.pts)
