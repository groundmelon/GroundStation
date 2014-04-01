# -*- coding: utf-8 -*- 
'''
Created on 2014-1-6

@author: GroundMelon
'''

import wx
import serial
from imageprocess.ImageCapture import ImageCapture
#from GroundStationBase import FrameGroundStationBase
from SerialSettingDialog import SerialSetting
from VideoSettingDialog import VideoSetting
import util
from util import DBGException
from Definition import *

class ButtonBlock():
    def open_xbee(self, comp):
        try:
            self.comm.open(self.comm_options)
            self.enable_comm_relative_components(True)
            self.sbar.update(u'XBee通信已经开启')
            self.add_work(DISPLAY_XBEE_DATA)
        except serial.SerialException,e:
            wx.MessageBox(u"串口可能已经被占用！\n%s"%str(e), u"串口开启错误",wx.OK | wx.ICON_ERROR)
            self.sbar.update(str(e),0)  
        except DBGException,e:
            wx.MessageBox(str(e), u"出现错误",wx.OK | wx.ICON_ERROR)
            self.sbar.update(str(e),0)
            self.comm.close()
        else:
            util.toggle_button(comp, u'开始', u'结束')

    def close_xbee(self, comp):
        try:
            if self.m_button_update_uavinfo.is_running:
                self.unshow_uavinfo(self.m_button_update_uavinfo)
                
            self.comm.close()
            self.enable_comm_relative_components(False)
            self.sbar.update(u'XBee通信已经关闭')
            self.remove_work(DISPLAY_XBEE_DATA)
        except DBGException,e:
            wx.MessageBox(str(e), u"出现错误",wx.OK | wx.ICON_ERROR)
            self.SetStatusText(str(e),0)
        else:
            util.toggle_button(comp, u'开始', u'结束')
            
    def open_video(self, comp):
        try:
            self.enable_video_components(True)
            self.enable_track_components(True)
            #self.camcap = WebcamService(self.m_bitmap_video.GetSize())
            self.camcap = ImageCapture(self.cap_dev_num)
            self.add_work(DISPLAY_VIDEO)
            self.sbar.update(u'图像传输已经打开')
        except DBGException,e :#Exception,e:
            wx.MessageBox(str(e), u"出现错误",wx.OK | wx.ICON_ERROR)
            self.SetStatusText(str(e),0)
        else:    
            util.toggle_button(comp, u'开始', u'结束')
            
    def close_video(self, comp):
        try:
            self.close_independent_video()
            if self.m_button_record.is_running:
                self.stop_record(self.m_button_record)
            #close track
            #close track video
            self.sbar.update(u'图像传输已经关闭')
            if self.m_button_toggle_track_video.is_running:
                self.close_track_video(self.m_button_toggle_track_video)
            self.enable_video_components(False)
            self.camcap.release()
            self.dc_video.DrawBitmap(util.get_null_bitmap(), 0, 0)
            self.remove_work(DISPLAY_VIDEO)
        except DBGException,e:
            wx.MessageBox(str(e), u"出现错误",wx.OK | wx.ICON_ERROR)
            self.SetStatusText(str(e),0)
        else:
            util.toggle_button(comp, u'开始', u'结束')
    
    def show_xbee_option(self):
        dlg = SerialSetting(self, self.comm_options)
        if dlg.ShowModal() == wx.ID_OK:
            self.comm_options = dlg.get_options()
        dlg.Destroy()
    
    def show_video_option(self):
        dlg = VideoSetting(self)
        if dlg.ShowModal() == wx.ID_OK:
            self.cap_dev_num = dlg.get_dev_num()
        dlg.Destroy()
    
    def show_uavinfo(self, comp):
        self.add_work(DISPLAY_UAVINFO)
        util.toggle_button(comp, u'开始', u'结束')
        self.m_button_save_uav_info.Enable(False)
    
    def unshow_uavinfo(self, comp):
        self.remove_work(DISPLAY_UAVINFO)
        util.toggle_button(comp, u'开始', u'结束')
        self.m_button_save_uav_info.Enable(True)

