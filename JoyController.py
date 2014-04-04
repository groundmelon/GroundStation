# -*- coding: utf-8 -*- 
'''
Created on 2014-4-2

@author: GroundMelon
'''
import pygame

class JoyCtrl():
    def __init__(self):
        pygame.init()
        pygame.joystick.init()
        assert pygame.joystick.get_count()!=0, 'NOJOYSTICK'
        self.js = pygame.joystick.Joystick(0)
        self.js.init()
    
    def release(self):
        pygame.joystick.quit()
        pygame.quit()
    
    def refresh_event(self):
        pygame.event.get()
    
    def get_axis(self):
        self.refresh_event()
        rtn = {'roll':0, 'pitch':0, 'yaw':0, 'throttle':0}
        rtn['roll'] = self.js.get_axis(0)*500+1500
        rtn['pitch'] = -self.js.get_axis(1)*500+1500
        rtn['yaw'] = -self.js.get_axis(3)*500+1500
        rtn['throttle'] = -self.js.get_axis(2)*500+1500
        return rtn
    
    def get_button(self):
        self.refresh_event()
        rtn = {}
        for i in range(12):
            rtn[str(i+1)] = self.js.get_button(i)
        return rtn
    
    def get_hat(self):
        self.refresh_event()
        rtn = self.js.get_hat(0)
        return rtn