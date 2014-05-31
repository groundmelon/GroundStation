# -*- coding: utf-8 -*- 
'''
按钮功能区

Created on 2014-1-6

@author: GroundMelon
'''

import wx
import serial
from imageprocess.ImageCapture import ImageCapture
from GroundStationBase import FrameGroundStationBase
from SerialSettingDialog import SerialSetting
from VideoSettingDialog import VideoSetting
import util
from util import DBGException
from Definition import *

class ButtonBlock(FrameGroundStationBase,object):
    '''
    按钮功能区
    
    包含一些最表层按钮，左上角按钮的回调函数
    '''
    def open_xbee(self, comp):
        '''
        打开XBee
        
            -打开串口
            -使能相关部件
            -添加相应功能到工作列表
            -改变按钮形态
        @param comp: 该按钮实例，用于改变按钮形态，比如颜色和label等
        '''
        try:
            self.comm.open(self.comm_options)
            self.enable_comm_relative_components(True)
            self.sbar.update(u'XBee通信已经开启')
            self.add_work(DISPLAY_XBEE_DATA)
        except serial.SerialException,e:
            wx.MessageBox(u"不存在指定串口 或 指定串口已被占用！\n%s"%str(e), u"串口开启错误",wx.OK | wx.ICON_ERROR)
            self.sbar.update(str(e),0)  
        except Exception:
            raise # 继续向上传递异常
        else:
            util.toggle_button(comp, u'开始', u'结束')

    def close_xbee(self, comp):
        '''
        关闭XBee
        
            -若正在更新无人机信息，则停止
            -若正在更使用JoyStick控制飞机，则停止
            -若正在跟踪，则停止
            -失能相关部件
            -关闭串口
            -改变按钮形态
        @param comp: 该按钮实例，用于改变按钮形态，比如颜色和label等
        '''
        try:
            if self.m_button_update_uavinfo.is_running:
                self.unshow_uavinfo(self.m_button_update_uavinfo)
            if self.m_button_toggle_joystick.is_running:
                self.close_joystick(self.m_button_toggle_joystick)
            if self.m_button_toggle_track.is_running:
                self.stop_track(self.m_button_toggle_track)
            
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
        '''
        打开视频传输
        
            -打开视频采集设备
            -初始化视频缓冲供视频滤波器使用
            -使能视频相关部件
            -使能跟踪相关部件
            -添加相应功能到工作列表
            -改变按钮形态
        @param comp: 该按钮实例，用于改变按钮形态，比如颜色和label等
        '''
        try:
            self.camcap = ImageCapture(self.cap_dev_num)
            self.cambuf=[] #视频滤波器使用的缓冲
            self.enable_video_components(True)
            self.enable_track_components(True)
            self.add_work(DISPLAY_VIDEO)
            self.sbar.update(u'图像传输已经打开')
        except ImageCapture.NoDeviceError:
            wx.MessageBox(u'设备号<%d>对应的设备不存在！'%self.cap_dev_num, u"出现错误",wx.OK | wx.ICON_ERROR)
            self.SetStatusText(u'设备号<%d>对应的设备不存在！'%self.cap_dev_num, 0)
        except Exception:
            raise # 继续向上传递异常
        else:    
            util.toggle_button(comp, u'开始', u'结束')
            
    def close_video(self, comp):
        '''
        关闭视频传输
        
            -关闭大窗口显示
            -停止录像
            -若正在跟踪，则停止
            -失能相关部件
            -释放摄像头，绘制无信号图像
            -改变按钮形态
        @param comp: 该按钮实例，用于改变按钮形态，比如颜色和label等
        '''
        try:
            self.close_independent_video()
            if self.m_button_record.is_running:
                self.stop_record(self.m_button_record)
            # close track video
            if self.m_button_toggle_track_video.is_running:
                self.close_track_video(self.m_button_toggle_track_video)
            self.enable_video_components(False)
            self.camcap.release()
            self.dc_video.DrawBitmap(util.get_null_bitmap(), 0, 0)
            self.remove_work(DISPLAY_VIDEO)
            self.sbar.update(u'图像传输已经关闭')
        except Exception:
            raise # 继续向上传递异常
        else:
            util.toggle_button(comp, u'开始', u'结束')
    
    def show_xbee_option(self):
        '''
        弹出XBee设置窗口
        '''
        dlg = SerialSetting(self, self.comm_options)
        if dlg.ShowModal() == wx.ID_OK:
            self.comm_options = dlg.get_options()# 获取子窗口中的设置信息
        dlg.Destroy()
    
    def show_video_option(self):
        '''
        弹出视频设置窗口
        '''
        dlg = VideoSetting(self, self.cap_dev_num)
        if dlg.ShowModal() == wx.ID_OK:
            self.cap_dev_num = dlg.get_dev_num()# 获取子窗口中的设置信息
        dlg.Destroy()
    
    def show_uavinfo(self, comp):
        '''
        显示UAV信息
        '''
        self.add_work(DISPLAY_UAVINFO)
        util.toggle_button(comp, u'开始', u'结束')
        self.m_button_save_uav_info.Enable(False)
    
    def unshow_uavinfo(self, comp):
        '''
        停止UAV信息的显示
        '''
        self.remove_work(DISPLAY_UAVINFO)
        util.toggle_button(comp, u'开始', u'结束')
        self.m_button_save_uav_info.Enable(True)

