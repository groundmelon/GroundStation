# -*- coding: utf-8 -*- 
'''
Created on 2014-3-23

@author: GroundMelon
'''
import wx
import util
from Definition import *
from BigVideoDisplay import VideoDisplayFrame
from imageprocess.MovieRecord import Record

class VideoBlock():
    def show_independent_video(self):
        if self.video_window is None:
            self.video_window = VideoDisplayFrame(self)
            self.video_window.Show()
            self.add_work(DISPLAY_INDEPENDENT_VIDEO)
        else:
            wx.MessageBox(u'无法打开多个独立播放窗口', u'错误',wx.OK | wx.ICON_ERROR)
            
    def close_independent_video(self):
        if self.video_window is not None:
            self.video_window.OnClose(None)
    
    def init_record(self, path):
        try:
            # 释放已有的mov_rec
            try:
                self.mov_rec.stop()
            except AttributeError:
                pass
            
            self.mov_rec = Record(path, 24.0, self.camcap.get_frame_size())
            self.m_button_record.Enable(True)
        except AssertionError,e:
            wx.MessageBox(str(e), u'错误',wx.OK | wx.ICON_ERROR)      
    
    def start_record(self, comp):
        try:
            self.mov_rec.touch()
            self.add_work(RECORD_VIDEO)
            util.toggle_button(comp, u'开始', u'结束')
            self.m_filePicker_output.Enable(False)
        except AssertionError,e:
            wx.MessageBox(str(e), u'错误',wx.OK | wx.ICON_ERROR)
        
    
    def stop_record(self, comp):
        self.remove_work(RECORD_VIDEO)
        self.mov_rec.stop()
        util.toggle_button(comp, u'开始', u'结束')
        self.m_button_record.Enable(False)
        self.m_filePicker_output.Enable(True)