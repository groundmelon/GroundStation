# -*- coding: utf-8 -*- 
'''
Created on 2014-1-3

@author: GroundMelon
@note: 处理跟踪相关处理
'''
from GroundStationBase import FrameGroundStationBase
import wx
import util
from Definition import *
# import imageprocess.ObjectTrackingSingleProcess as Objtrack
# import imageprocess.ObjectTrackingMultiProcess as Objtrack
import imageprocess.ObjectTracking as Objtrack

from TrackAlgorithm import TrackController

class DragInfomation(object):
        '''拖拽信息类，存储处理拖拽信息
        '''
        def start_drag(self, start_pos):
            self.start = util.Point(start_pos)
            self.cur = util.Point(start_pos)
        
        def update_cur_pos(self, cur_pos):
            self.cur = util.Point(cur_pos)
            
        def get_drag_data(self):
            return{'start':self.start, 'end':  self.cur}

class TrackBlock():
    def enable_track_components(self, switch):
        self.m_panel_track.Enable(switch)
        for each in self.m_panel_track.GetChildren():
            each.Enable(switch)
        self.m_button_select_object.Enable(False)
        self.m_button_toggle_track.Enable(False)
        
    
    def open_track_video(self, comp):
        self.track_image_adjust_value = Objtrack.get_image_adjust_value()
        self.add_work(DISPLAY_TRACK_VIDEO)
        self.display_track_state = DISPLAY_TRACK_STATE_RAW
        util.toggle_button(comp, u'显示视频', u'关闭显示')
        self.m_button_select_object.Enable(True)
            
    def close_track_video(self, comp):
        self.remove_work(DISPLAY_TRACK_VIDEO)
        self.display_track_state = None
        self.dc_track.DrawBitmap(util.get_null_bitmap(), 0, 0)
        util.toggle_button(comp, u'显示视频', u'关闭显示')
        self.m_button_select_object.Enable(False)
        if self.m_button_toggle_track.is_running:   
            self.stop_track(self.m_button_toggle_track)
        self.m_button_toggle_track.Enable(False)
    
    def stop_track(self, comp):
        
        self.remove_work(TRACK_OBJECT)
        util.toggle_button(comp, u'开始', u'结束')
        self.m_button_select_object.Enable(True)
    
    def start_track(self, comp):
        self.add_work(TRACK_OBJECT)
        util.toggle_button(comp, u'开始', u'结束')
        self.m_button_select_object.Enable(False)
        self.trackctrl = TrackController(self.camcap.get_frame_size())
        
    def set_track_arg(self, s):
        sel = self.m_choice_track_arg.GetStringSelection()
        if 'multi' == sel:
            self.multimean_arg = float(s)
        elif 'edge' == sel:
            self.edge_arg = float(s)
        
# ---- 图像调整相关函数 ----
    def get_adjusted_image(self, src):    
        return Objtrack.get_adjusted_image(src, self.track_image_adjust_value)
        
    def change_adjust_type(self):
        choice = self.m_radioBox_image_adj.GetStringSelection()
        self.m_staticText_adjust_type.SetLabel(choice)
        self.m_slider_adjust.SetValue(self.track_image_adjust_value[choice])
    
    def change_adjust_value(self):
        choice = self.m_radioBox_image_adj.GetStringSelection()
        self.track_image_adjust_value[choice] = self.m_slider_adjust.GetValue()

# ---- 框选目标相关函数 ----    
    def toggle_drag_selection(self, toggle):
        if toggle: # pressed button, start dragging
            self.display_track_state = DISPLAY_TRACK_STATE_RAW
            self.m_bitmap_track.Bind( wx.EVT_LEFT_DOWN, self.on_track_bitmap_left_down )
            self.m_bitmap_track.Bind( wx.EVT_LEFT_UP, self.on_track_bitmap_left_up )           
            self.SetCursor(wx.StockCursor( wx.CURSOR_CROSS ) )
            self.drag_info = DragInfomation()
            self.sbar.update(u'请使用鼠标左键拖拽选择目标')
        else:   #end dragging
            self.m_bitmap_track.Bind( wx.EVT_LEFT_DOWN, None)
            self.m_bitmap_track.Bind( wx.EVT_LEFT_UP, None)
            self.m_bitmap_track.Bind( wx.EVT_MOTION, None)       
            self.SetCursor(wx.StockCursor(wx.CURSOR_ARROW))
            self.display_track_state = DISPLAY_TRACK_STATE_RESULT
            self.sbar.update(u'目标已经选择')
            
    
    def start_drag(self, event):# left key is pressed
        self.drag_info.start_drag(event.GetPositionTuple())
        self.m_bitmap_track.Bind( wx.EVT_MOTION, self.on_track_bitmap_motion )
        self.display_track_state = DISPLAY_TRACK_STATE_SELECTION
        self.frozen_frame = self.camcap.get_frame()
        self.sbar.update(u'按住左键拖拽')
        
    def on_drag(self, event):
        self.drag_info.update_cur_pos(event.GetPositionTuple())
    
    def end_drag(self, event):
        self.drag_info.update_cur_pos(event.GetPositionTuple())
        rect = Objtrack.get_selection_rect(self.frozen_frame.shape, 
                                           self.drag_info.get_drag_data(),
                                           self.bitmap_track_size)
        try:
#             self.objmatch = Objtrack.ObjectMatch(rect, self.frozen_frame, self.get_hist_channel())
            self.objmatch = Objtrack.ObjectTrack(rect, self.frozen_frame, self.get_hist_channel())
            self.frozen_frame = None
            self.drag_info = None
            self.toggle_drag_selection(False)
            self.m_button_toggle_track.Enable(True)
        except AssertionError,e:
            wx.MessageBox(str(e), u"出现错误",wx.OK | wx.ICON_ERROR)
            self.sbar.update(unicode(e))
            self.frozen_frame = None
            self.drag_info = None
            self.toggle_drag_selection(False)
            self.display_track_state = DISPLAY_TRACK_STATE_RAW      
            
    def get_dragging_image(self, src, drag_data):
        return Objtrack.get_dragging_image(src, drag_data, self.bitmap_track_size)