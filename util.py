# -*- coding: utf-8 -*- 
'''
Created on 2014-1-4

@author: GroundMelon
'''

import wx
import cv2
import numpy as np
import time

DEBUG = True

if DEBUG:
    DBGException = None
else:
    DBGException = Exception

def get_now():
    return time.strftime('%c')

TEXTSIZE = None
PADDING = None
WXFONT = None
TIME_TEXT_WIDTH = None
def init_font():
    global TEXTSIZE
    global PADDING
    global WXFONT
    global TIME_TEXT_WIDTH
    TEXTSIZE = (9, 16)
    PADDING = 10
    WXFONT = wx.Font( 10, wx.MODERN, wx.NORMAL, wx.NORMAL, False, "Consolas" )
    #WXFONT.SetPixelSize(TEXTSIZE)
    TIME_TEXT_WIDTH = len(get_now()) * TEXTSIZE[0]
    return

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
            self.output_str = '%s: %s'%(arg[0].ljust(6), arg[1])
    
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
    #img = cv2.cvtColor(np.uint8(cvimg), cv2.cv.CV_BGR2RGB)
    img = cv2.cvtColor(np.uint8(cvimg), cv2.COLOR_BGR2RGB)
    bmp = wx.BitmapFromBuffer(img.shape[1], img.shape[0], img )
    return bmp

def wxbmp_to_cvimg(wxbmp):
    shape = (wxbmp.Size[1], wxbmp.Size[0],3)
    buf = np.ndarray(shape, dtype=np.uint8)
    wxbmp.CopyToBuffer(buf, wx.BitmapBufferFormat_RGB)
    cvimg = cv2.cvtColor(buf, cv2.COLOR_RGB2BGR)
    
    return cvimg

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
    def __init__(self, s='Noname', display = True):
        self.start_time = time.clock()
        self.s = s
        self.display = display
    def stop(self):
        if self.display:
            now_time = time.clock()
            #print('[%s] %.3fms'%(self.s,(now_time-self.start_time)*1000))
    def pause(self):
        if self.display:
            now_time = time.clock()
            #print('[%s P] %.3fms'%(self.s,(now_time-self.start_time)*1000))
        
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
            assert isinstance(arg[0][0], (int,float)), "arg tuple[0] is not int or float"
            assert isinstance(arg[0][1], (int,float)), "arg tuple[1] is not int or float"
            self.x = arg[0][0]
            self.y = arg[0][1]
        elif arglen == 2:
            assert isinstance(arg[0], (int,float)), "arg x is not int or float"
            assert isinstance(arg[1], (int,float)), "arg y is not int or float"
            self.x = arg[0]
            self.y = arg[1]
        else:
            assert False,"Invalid args"
        
        self.tup = (self.x, self.y) # tuple represent
    def __repr__(self):
        return '<pt(%.2f,%.2f)>'%(self.x, self.y)

JSCODES = '''
            // Get the current view.
            var lookAt = ge.getView().copyAsLookAt(ge.ALTITUDE_RELATIVE_TO_GROUND);
            var camera = ge.getView().copyAsCamera(ge.ALTITUDE_RELATIVE_TO_GROUND);
            var la = %f;
            var lo = %f;
            var rg = %f;
            
            
            // Set the FlyTo speed.
            ge.getOptions().setFlyToSpeed(1.0);
            // Set new latitude and longitude values.
            lookAt.setLatitude(la);
            lookAt.setLongitude(lo);
            lookAt.setRange(rg);
            
            // Update the view in Google Earth.
            ge.getView().setAbstractView(lookAt);
            //ge.getView().setAbstractView(camera);
            
            var old = ge.getFeatures().getLastChild();
            if (old){
                ge.getFeatures().removeChild(old);
            }
            
            placemark.setStyleSelector(style); //apply the style to the placemark
            
            // Set the placemark's location.  
            point.setLatitude(la);
            point.setLongitude(lo);
            placemark.setGeometry(point);
            
            // Add the placemark to Earth.
            ge.getFeatures().appendChild(placemark);
        '''
JSCODESINIT = '''
            // Get the current view.
            var lookAt = ge.getView().copyAsLookAt(ge.ALTITUDE_RELATIVE_TO_GROUND);
            var camera = ge.getView().copyAsCamera(ge.ALTITUDE_RELATIVE_TO_GROUND);
            var la = %f;
            var lo = %f;
            var rg = %f;
            

            // Set the FlyTo speed.
            ge.getOptions().setFlyToSpeed(1.0);
            // Set new latitude and longitude values.
            lookAt.setLatitude(la);
            lookAt.setLongitude(lo);
            lookAt.setRange(rg);
            
            // Update the view in Google Earth.
            ge.getView().setAbstractView(lookAt);
            //ge.getView().setAbstractView(camera);
            
            // Create the placemark.
            var placemark = ge.createPlacemark('');
            placemark.setName("");
            
            // Define a custom icon.
            var icon = ge.createIcon('');
            icon.setHref("http://maps.google.com/mapfiles/kml/paddle/red-circle.png");
            var style = ge.createStyle(''); //create a new style
            style.getIconStyle().setIcon(icon); //apply the icon to the style
            placemark.setStyleSelector(style); //apply the style to the placemark
            
            // Set the placemark's location.  
            var point = ge.createPoint('');
            point.setLatitude(la);
            point.setLongitude(lo);
            placemark.setGeometry(point);
            
            // Add the placemark to Earth.
            ge.getFeatures().appendChild(placemark);
        '''

if __name__ == '__main__':
    print(Point(1,2))
    print(Point((3,4)))
            