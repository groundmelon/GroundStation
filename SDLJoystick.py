# -*- coding: utf-8 -*- 
'''
Created on 2014-4-8

@author: GroundMelon
'''

import sdl2
import sdl2.ext

class SDLJoystick():
    def __init__(self):
        sdl2.SDL_Init(sdl2.SDL_INIT_JOYSTICK)
    
    def get_count(self):
        return sdl2.joystick.SDL_NumJoysticks()
    
    def refresh_event(self):
        sdl2.ext.get_events()
    
    def init_joy(self, num):
        self.ptrJOY = sdl2.joystick.SDL_JoystickOpen(num)
        assert self.ptrJOY, 'Open fail.'
    
    def get_axis(self, axis_num):
        assert self.ptrJOY, 'Joystick is Closed.'
        return sdl2.joystick.SDL_JoystickGetAxis(self.ptrJOY, axis_num)
    
    def get_button(self, btn_num):
        assert self.ptrJOY, 'Joystick is Closed.'
        return sdl2.joystick.SDL_JoystickGetButton(self.ptrJOY, btn_num)
    
    def get_hat(self, hat_num):
        assert self.ptrJOY, 'Joystick is Closed.'
        val = sdl2.joystick.SDL_JoystickGetHat(self.ptrJOY, hat_num)
        return (((val>>1)%2)*1+((val>>3)%2)*-1, (val%2)*1+((val>>2)%2)*-1)
    
    def quit(self):
        sdl2.joystick.SDL_JoystickClose(self.ptrJOY)
        sdl2.SDL_Quit()
        
    def __del__(self):
        self.quit()
    

if __name__ == '__main__':
    SDLJoy = SDLJoystick()
    raw_input('Find %d devices.'%SDLJoy.get_count())
    joy = SDLJoy.init_joy(0)
    while True:
        print SDLJoy.refresh_event(),
        print joy.get_hat(0)
    del SDLJoy
    
    