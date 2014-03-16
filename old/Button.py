# -*- coding: utf-8 -*- 
'''
Created on 2013-12-5

@author: GroundMelon
'''
import wx
import serial
from imageprocess.test import WebcamService

def open_xbee(window, comp):
    try:
        window.comm.open(window.comm_options)
    except serial.SerialException,e:
        wx.MessageBox("串口可能已经被占用！\n%s"%str(e), u"串口开启错误",wx.OK | wx.ICON_ERROR)
        window.SetStatusText(str(e),0)  
    except Exception,e:
        wx.MessageBox(str(e), u"出现错误",wx.OK | wx.ICON_ERROR)
        window.SetStatusText(str(e),0)
        window.comm.close()
    else:
        comp.SetBackgroundColour('#00FF00')
        comp.SetLabel(comp.GetLabel().replace(u'开始',u'结束'))
        window.xbee_comm_state = not window.xbee_comm_state
    
    

def close_xbee(window, comp):
    try:
        window.comm.close()
    except Exception,e:
        wx.MessageBox(str(e), u"出现错误",wx.OK | wx.ICON_ERROR)
        window.SetStatusText(str(e),0)
    else:
        comp.SetBackgroundColour(wx.NullColor)
        comp.SetLabel(comp.GetLabel().replace(u'结束',u'开始'))
        window.xbee_comm_state = not window.xbee_comm_state
        
def open_video(window, comp):
    try:
        window.webcam = WebcamService1(window.m_bitmap_video.GetSize())
    except AssertionError, e: #Exception,e:
        wx.MessageBox(str(e), u"出现错误",wx.OK | wx.ICON_ERROR)
        window.SetStatusText(str(e),0)
    else:    
        comp.SetBackgroundColour('#00FF00')
        comp.SetLabel(comp.GetLabel().replace(u'开始',u'结束'))
        window.video_on = not window.video_on
        
def close_video(window, comp):
    try:
        window.webcam.release()
        window.dc.Clear()
    except AssertionError, e: #Exception,e:
        wx.MessageBox(str(e), u"出现错误",wx.OK | wx.ICON_ERROR)
        window.SetStatusText(str(e),0)
    else:
        comp.SetBackgroundColour(wx.NullColor)
        comp.SetLabel(comp.GetLabel().replace(u'结束',u'开始'))
        window.video_on = not window.video_on
    