# -*- coding: utf-8 -*- 
'''
Created on 2014-4-2

@author: GroundMelon
'''
import pygame
from SDLJoystick import SDLJoystick
import time

VAL = 0
STATE = 1
TIM = 2

NORMAL = 0
CHANGING = 1

DELAY = 20/1000.0

tmp=[]

# class JoyCtrl1():
#     def __init__(self):
#         pygame.init()
#         pygame.joystick.init()
#         assert pygame.joystick.get_count()!=0, 'NOJOYSTICK'
#         self.js = pygame.joystick.Joystick(0)
#         self.js.init()
#         self._btninfo = [{VAL:0, STATE:NORMAL, TIM:0.0} for i in range(12)]
#         self._toggle_info = {'sd':0,
#                             }
#     
#     def release(self):
#         pygame.joystick.quit()
#         pygame.quit()
#         
#     def get_ctrl(self):
#         self.refresh_event()
#         rtn = {'roll':0, 'pitch':0, 'yaw':0,} #'throttle':0}
#         rtn['roll'] = self.js.get_axis(0)*166+1500 +2
#         rtn['pitch'] = -self.js.get_axis(1)*166+1500 -1
#         rtn['yaw'] = -self.js.get_axis(3)*166+1500 -1
#         rtn['throttle'] = self.js.get_hat(0)[1] * 250 + 1500
#         
#         rst = self.get_btn()
#         rtn['ctrltype'] = rst[0]
#         rtn['sd'] = self._toggle('sd', rst[2])
#         
#         return rtn
#     
#     def _toggle(self, key, val):
#         if self._toggle_info[key] != val:
#             self._toggle_info[key] = val
#             if val == 1:
#                 return True
#             else:
#                 return False
#         else:
#             return False
#     
#     def refresh_event(self):
#         pygame.event.get()
#     
#     def get_axis(self):
#         self.refresh_event()
#         rtn = {'roll':0, 'pitch':0, 'yaw':0,} #'throttle':0}
#         rtn['roll'] = self.js.get_axis(0)*166+1500 +2
#         rtn['pitch'] = -self.js.get_axis(1)*166+1500 -1
#         rtn['yaw'] = -self.js.get_axis(3)*166+1500 -1
#         #rtn['throttle'] = -self.js.get_axis(2)*500+1500
#         return rtn
#     
#     def get_button(self):
#         self.refresh_event()
#         rtn = [9]*12
#         for i in range(12):
#             val = self.js.get_button(i)
#             rtn[i] = val
#         return rtn
#     
#     def get_hat(self):
#         self.refresh_event()
#         rtn = self.js.get_hat(0)[1]
#         return rtn
#     
#     def get_btn(self):
#         self.refresh_event()
#         rtn = [9]*12
#         for i in range(2):
#             val = self.js.get_button(i)
#             if self._btninfo[i][STATE] == NORMAL:
#                 if val != self._btninfo[i][VAL]:
#                     self._btninfo[i][STATE] = CHANGING
#                     self._btninfo[i][TIM] = time.clock() + DELAY
#             elif self._btninfo[i][STATE] == CHANGING:
#                 if val == self._btninfo[i][VAL]:
#                     self._btninfo[i][STATE] = NORMAL
#                 if val != self._btninfo[i][VAL] and time.clock() >= self._btninfo[i][TIM]:
#                     self._btninfo[i][STATE] = NORMAL
#                     self._btninfo[i][VAL] = val
#             rtn[i] = self._btninfo[i][VAL] 
#         return rtn

class JoyCtrl():
    def __init__(self):
        self.js = SDLJoystick()
        assert self.js.get_count()!=0, 'NOJOYSTICK'
        self.js.init_joy(0)
        self._btninfo = [{VAL:0, STATE:NORMAL, TIM:0.0} for _ in range(12)]
        self._toggle_info = {'sd':0,
                            }
        self.ctrls = {'roll':1500, 'pitch':1500, 'yaw':1500, 'throttle':1500,
                      'ctrltype':0, 'sd':0}
    
    def release(self):
        self.js.quit()
        
    def get_ctrl(self):
        self.refresh_event()
        self.ctrls['roll'] = +(self.js.get_axis(0)+256) / 200 + 1500
        self.ctrls['pitch'] = -(self.js.get_axis(1)+256) / 200 + 1500
        self.ctrls['yaw'] = -(self.js.get_axis(3)+256) / 200 + 1500
        self.ctrls['throttle'] = self.js.get_hat(0)[1] * 250 + 1500
        
        rst = self.get_btn()
        self.ctrls['ctrltype'] = rst[0]
        self.ctrls['sd'] = int(not self.ctrls['sd']) if self._if_rising('sd', rst[2]) else self.ctrls['sd']
        
        
        return self.ctrls
    
    def _if_rising(self, key, val):
        if self._toggle_info[key] != val:
            self._toggle_info[key] = val
            if val == 1:
                return True
            else:
                return False
        else:
            return False
    
    def refresh_event(self):
        self.js.refresh_event()
    
    def get_button(self):
        ''' 获得按钮状态，无消抖功能
        '''
        #self.refresh_event()
        rtn = [9]*12
        for i in range(12):
            val = self.js.get_button(i)
            rtn[i] = val
        return rtn
    
    def get_btn(self):
        ''' 获得按钮状态，有消抖功能
        '''
        self.refresh_event()
        rtn = [9]*12
        for i in range(12):
            val = self.js.get_button(i)
            if self._btninfo[i][STATE] == NORMAL:
                if val != self._btninfo[i][VAL]:
                    self._btninfo[i][STATE] = CHANGING
                    self._btninfo[i][TIM] = time.clock() + DELAY
            elif self._btninfo[i][STATE] == CHANGING:
                if val == self._btninfo[i][VAL]:
                    self._btninfo[i][STATE] = NORMAL
                if val != self._btninfo[i][VAL] and time.clock() >= self._btninfo[i][TIM]:
                    self._btninfo[i][STATE] = NORMAL
                    self._btninfo[i][VAL] = val
            rtn[i] = self._btninfo[i][VAL] 
        return rtn
        

if __name__ == '__main__':
    joy = JoyCtrl()
    while True:
        rtn = joy.get_btn()
        print(rtn)
