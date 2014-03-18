# -*- coding: utf-8 -*- 
'''
Created on 2014-1-4

@author: GroundMelon
'''

import wx
import cv2
import numpy as np
import time
from Gnuplot.termdefs import Arg
from Cython.Plex.Regexps import Str

DEBUG = True

if DEBUG:
    DBGException = None
else:
    DBGException = Exception

class InfoEntry(object):
    TYPE_LABEL = 1
    TYPE_WARNING = 0
    def __init__(self, type, *arg):
        arglen = len(arg)
        assert arglen > 0, 'arg length must > 0.'
        self.type = type
        if arglen == 1:
            assert isinstance(arg[0], str), 'arg[0] must be string.'
            self.label = arg[0]
            self.output_str = '%s'%(arg[0])
        elif arglen == 2:
            assert isinstance(arg[0], str) and isinstance(arg[1], str), 'arg[0,1] must be string.'
            self.label = arg[0]
            self.value = arg[1]
            self.output_str = '%s:%s'%(arg[0].ljust(8), arg[1])
    
    def __repr__(self):
        return self.output_str

def toggle_button(comp, stop_label, running_label):
    if comp.is_running:
        comp.SetBackgroundColour(wx.NullColour)
        comp.SetLabel(comp.GetLabel().replace(running_label,stop_label))
    else:#comp.is_runnung == False
        comp.SetBackgroundColour('#00FF00')
        comp.SetLabel(comp.GetLabel().replace(stop_label,running_label))    
    comp.is_running = not comp.is_running

def cvimg_to_wxbmp(cvimg):        
    img = cv2.cvtColor(np.uint8(cvimg), cv2.cv.CV_BGR2RGB)
    bmp = wx.BitmapFromBuffer(img.shape[1], img.shape[0], img )
    return bmp

def cvimg_resize(cvimg, size):
    return cv2.resize(cvimg, size, interpolation = cv2.INTER_CUBIC)

def cvimg_rescale(cvimg, scale):
    if scale < 1:
        return cv2.resize(cvimg, (0,0) , fx=scale, fy=scale, interpolation = cv2.INTER_AREA)
    elif scale > 1:
        return cv2.resize(cvimg, (0,0) , fx=scale, fy=scale, interpolation = cv2.INTER_LINEAR)
    elif scale == 1:
        return cvimg


class SW(object):
    ''' stop watch '''
    def __init__(self, s='Noname'):
        self.start_time = time.clock()
        self.s = s
    def stop(self, *arg):
        now_time = time.clock()
        print('[%s] %.3fms'%(self.s,(now_time-self.start_time)*1000))
        
NULLIMG = r'resources\null.bmp'
def get_null_bitmap():
    return wx.BitmapFromImage(wx.Image(NULLIMG))

class Point(object):
    def __init__(self, *arg):
        arglen = len(arg)
        if arglen == 0:
            self.x = 0
            self.y = 0
        elif arglen == 1:
            assert isinstance(arg[0], tuple), "arg is not tuple"
            assert isinstance(arg[0][0], int), "arg tuple[0] is not int"
            assert isinstance(arg[0][1], int), "arg tuple[1] is not int"
            self.x = arg[0][0]
            self.y = arg[0][1]
        elif arglen == 2:
            assert isinstance(arg[0], int), "arg x is not int"
            assert isinstance(arg[1], int), "arg y is not int"
            self.x = arg[0]
            self.y = arg[1]
        else:
            assert False,"Invalid args"
        
        self.tup = (self.x, self.y) # tuple represent
    def __repr__(self):
        return '<util.Point(%d,%d)>'%(self.x, self.y)
        

if __name__ == '__main__':
    print(Point(1,2))
    print(Point((3,4)))
            