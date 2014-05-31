# -*- coding: utf-8 -*- 
'''
Created on 2013-12-4

@author: Administrator
'''
from GroundStationBase import FrameGroundStationBase
from TrackBlock import TrackBlock
from ButtonBlock import ButtonBlock
from MenuBlock import MenuBlock
from WorkBlock import WorkBlock
from VideoBlock import VideoBlock
from UAVControlBlock import UAVCtrlBlock
from ParameterAdjustBlock import ParameterAdjustBlock
from CommunicationBlock import CommBlock, InputHistory
#from attitude.attitudeMod import AttitudeDisplay
from UAVInfomation import UAVInfomation
from StatusBarSystem import StatusBarSystem


from communication.XBeeComm import XBee
import communication.MessageProcess as MsgPrcs
from imageprocess.ObjectTracking import img_filter

import util
import os
import sys
import wx
import wx.html2
import time
import math

from Definition import *
from imageprocess.ObjectTracking import METHOD


class GroundStation(WorkBlock ,TrackBlock, VideoBlock,
                    ButtonBlock, MenuBlock, CommBlock, ParameterAdjustBlock,
                    UAVCtrlBlock
                    ):
    def __init__(self):
        self.lasttime = time.clock()
        
        super(GroundStation, self).__init__(parent = None)
        self.SetIcon(wx.Icon(r'resources/gs.ico', wx.BITMAP_TYPE_ICO))              
        
        #---- init status bar system ----
        self.sbar = StatusBarSystem(self.m_statusBar)# 状态栏管理系统
        
        #---- add Google Earth Components ----  
        sizer_ge = self.m_panel_route.GetSizer()
        self.browser_ge = wx.html2.WebView.New(self.m_panel_route, size=(330,330))# Google Earth WebView Object'''
        sizer_ge.Add(self.browser_ge, 1, wx.ALIGN_CENTER, 0)
        self.browser_ge.LoadURL(r'file:///%s/resources/ge.html'%os.getcwd().replace('\\','/'))
        self.GE_uninited = True # GoogleEarth的显示未初始化
                
        #---- set record labels ----
        # 设置文件选择器按钮的Label
        self.m_filePicker_output.GetPickerCtrl().SetLabel(u'设置视频参数')
        
        #---- add component attributes ----
        # 对起切换作用的Buttons加上is_running属性方便操作
        for comp in [self.m_button_toggle_track, 
                     self.m_button_toggle_track_video,
                     self.m_button_toggle_video,
                     self.m_button_toggle_xbee,
                     self.m_button_update_uavinfo,
                     self.m_button_select_object,
                     self.m_button_record,
                     self.m_button_toggle_joystick,
                     ]:
            comp.__setattr__('is_running', False)

        #---- init comm block ----
        self.comm = XBee(self) # 通信模块
        self.comm_options = self.load_default_comm_options() # 读取默认通信设置
        self.history = InputHistory(self)# 串口发送区历史记录
        self.enable_comm_relative_components(False)
        
        #---- init video block ----
        self.cap_dev_num = DEFAULT_CAP_DEV_NUM
        self.enable_video_components(False)
        self.video_window = None
        
        #---- init track block ----
        self.enable_track_components(False)
        self.display_track_state = None
        
        #---- init parameter adjust block ----
        self.init_para_block()
        
        #---- init size variables ----
        self.bitmap_track_size = tuple(self.m_bitmap_track.GetSize())
        self.bitmap_video_size = tuple(self.m_bitmap_video.GetSize())
        
        #---- init UAVInformation ----
        self.UAVinfo = UAVInfomation()
        
        #---- init UAV Control ----
        self.init_uav_control()
        
        # --- dc init ---
        self.dc_video = wx.ClientDC(self.m_bitmap_video)
        self.dc_track = wx.ClientDC(self.m_bitmap_track)
        self.memory = wx.MemoryDC()
        self.dc_attitude = wx.ClientDC(self.m_bitmap_attitude)
        self.dc_uavinfo = wx.ClientDC(self.m_bitmap_uavinfo)
        
        # --- test ---
        self.multimean_arg = None
        self.edge_arg = None
        
        self.init_worklist()
        #self.Bind(wx.EVT_IDLE, self.main_work)
        self.timer = wx.Timer(self)
        self.Bind(wx.EVT_TIMER, self.main_work, self.timer)
        self.timer.Start(1000.0/TASK_HIGH_FREQ)
        self.timer.last_time=time.clock()
        
#         self.timer1 = wx.Timer(self) 
#         self.Bind(wx.EVT_TIMER, self.main_work1, self.timer1)
#         self.timer1.Start(1000/10)
        
        self.Bind(wx.EVT_CLOSE, self.OnClose)

        
#------ Menu binding function ------
    def on_about(self, event):
        self.about()
    
    def on_save_comm_option(self, event): 
        self.save_comm_option(self.comm_options)
    
    
    def on_load_comm_option(self, event):
        self.load_comm_option()
    
    def on_check_comm_option(self, event):
        self.load_default_comm_options()
        self.display_comm_option(self.comm_options)
    
#------ Button binding function ------   
    
    def on_xbee_option(self, event):
        self.show_xbee_option()
    
    def on_toggle_xbee(self, event):        
        if event.GetEventObject().is_running:
            self.close_xbee(event.GetEventObject())
        else:
            self.open_xbee(event.GetEventObject())
    
    def on_toggle_video(self, event):
        if event.GetEventObject().is_running:
            self.close_video(event.GetEventObject())
        else:
            self.open_video(event.GetEventObject())
    
    def on_video_comm_option(self, event):
        self.show_video_option()
    
    def on_update_uavinfo(self, event):
        if event.GetEventObject().is_running:
            self.unshow_uavinfo(event.GetEventObject())
        else:
            self.show_uavinfo(event.GetEventObject())
    
    def on_save_uav_info(self, event):
        saved = self.UAVinfo.save_to_file(self, pidpara = self.get_showing_para())
        if self.m_menuItem_clear_uav_info_after_save.IsChecked() and saved:
            self.UAVinfo.clear_buf()
        self.update_GUI_UAVinfo(self.UAVinfo.get())
    
    def on_clear_uav_info(self, event):
        self.UAVinfo.clear_buf()
        self.update_GUI_UAVinfo(self.UAVinfo.get())

#------ Video Binding Function ------    
    def on_video_window_show(self, event):
        self.show_independent_video()
        
    def on_record(self, event):
        if event.GetEventObject().is_running:
            self.stop_record(event.GetEventObject())
        else:
            self.start_record(event.GetEventObject())
    
    def on_record_file_changed(self, event):
        self.init_record(self.m_filePicker_output.GetPath())
    
    def on_enter_bitmap_video(self, event):
        self.sbar.update(u'提示：单击右键可选择OSD选项')
    
    def on_leave_bitmap_video(self, event):
        self.sbar.backward()

#------ UAV Control Binding Function ------
    def on_PT_send(self, event):
        rtn = self.send_pt_reference()
        self.sbar.update(u'云台控制信息已经发送(%d)'%rtn)
    
    def on_toggle_joystick(self, event):
        if event.GetEventObject().is_running:
            self.close_joystick(event.GetEventObject())
        else:
            self.open_joystick(event.GetEventObject())
    
    def on_toggle_smart_direction(self, event):
        self.toggle_smart_direction(self.m_checkBox_smart_direction.IsChecked())
        
#------ Track Binding Function ------   

    def on_toggle_track_video(self, event):
        if event.GetEventObject().is_running:
            self.close_track_video(event.GetEventObject())
        else:
            self.open_track_video(event.GetEventObject())
     
    def on_radiobox_adjust(self, event):
        self.change_adjust_type()
     
    def on_slider_adjust_changed(self, event):
        self.change_adjust_value()
     
    def on_select_object(self, event):
        self.toggle_drag_selection(True)
         
    def on_toggle_track(self, event):
        if event.GetEventObject().is_running:
            self.stop_track(event.GetEventObject())
        else:
            self.start_track(event.GetEventObject())
    
    def on_track_bitmap_left_down(self, event):
        self.start_drag(event)
     
    def on_track_bitmap_left_up(self, event):
        self.end_drag(event)
     
    def on_track_bitmap_motion(self, event):
        self.on_drag(event)
    
    def on_track_arg_enter(self, event):
        self.set_track_arg(event.GetEventObject().GetValue())
    
    def on_enter_bitmap_track(self, event):
        self.sbar.update(u'提示：单击右键可选择显示模式和分辨模式')
    
    def on_leave_bitmap_track(self, event):
        self.sbar.backward()

#------ Parameter Adjust Binding Function ------
    def on_send_para(self, event):
        self.send_para((self.m_checkBox_para_x.IsChecked(),
                        self.m_checkBox_para_y.IsChecked(),
                        self.m_checkBox_para_z.IsChecked(),
                        self.m_checkBox_para_h.IsChecked(),
                        self.m_checkBox_para_p.IsChecked(),
                        )
                       )
    
    def on_load_para(self, event):
        self.load_para()
    
    def on_save_para(self, event):
        self.save_para()
    
    def on_set_down_para(self, event):
        self.set_down_para()
    
    def on_update_pid(self, event):
        self.get_pid()

#------ Communication Binding Function ------   
    def on_send_area_enter(self, event):
        self.send_data_by_GUI()
    
    def on_send_comm_click(self, event):
        self.send_data_by_GUI()
    
    def on_send_area_char(self, event):
        keycode = event.GetKeyCode()
        if keycode == wx.WXK_UP:
            self.m_textCtrl_comm_send.SetValue(self.history.getByRel(-1))
            self.m_textCtrl_comm_send.SetInsertionPoint(len(self.m_textCtrl_comm_send.GetValue()))
        elif keycode == wx.WXK_DOWN:
            self.m_textCtrl_comm_send.SetValue(self.history.getByRel(1))
            self.m_textCtrl_comm_send.SetInsertionPoint(len(self.m_textCtrl_comm_send.GetValue()))
        else:
            FrameGroundStationBase.on_send_comm_char(self, event)
    
    def on_clear_receive(self, event):
        self.comm.clear_rcvbuf()
        self.update_rcv_area(refresh = True)
    
    def on_recv_style_choice(self, event):
        self.update_rcv_area(refresh = True)

        
#------ CallAfter Function ------
    def on_xbee_receive_char(self,rcvchr):
        self.comm.on_receive_char(rcvchr)
        msgtype, data = self.get_backdata()
        if data:
            self.process_backdata(msgtype, data)
     
    
#------ Work Function ------        
    def main_work(self, event):
        
        worklist = self.worklist
        a = time.clock()        
        
        # MAIN_TASK_FREQ Hz Tasks
        if USING_JOYSTICK in self.worklist:
                self.update_joy_status()
        
        if DISPLAY_VIDEO in worklist:
            srcimg = self.camcap.get_frame()
            if len(self.cambuf)==0:
                self.cambuf.append(srcimg)
                self.cambuf.append(srcimg)
#                 self.cambuf.append(srcimg)
#                 print('cambuf length:%d'%len(self.cambuf))

            wxbmp = util.cvimg_to_wxbmp(srcimg)
            wximg = wx.ImageFromBitmap(wxbmp)
            memvideo = wx.MemoryDC()
            memvideo.SelectObject(wxbmp)

            if self.m_menuItem_video_osd.IsChecked():
                # draw OSD information on bitmap_video
                memvideo.SetTextForeground( wx.BLUE )
                memvideo.SetFont( util.WXFONT )
                pos = (srcimg.shape[1] - util.PADDING - util.TIME_TEXT_WIDTH, util.PADDING)
                memvideo.DrawText(util.get_now(), pos[0], pos[1])

            # 设置缩放比例
            memvideo.SetUserScale(float(srcimg.shape[1])/float(self.bitmap_video_size[0]),
                                float(srcimg.shape[0])/float(self.bitmap_video_size[1])
                                )
            self.dc_video.Blit(0, 0, self.bitmap_video_size[0], self.bitmap_video_size[1], memvideo, 0, 0)
            memvideo.SelectObject(wx.NullBitmap)
            
        
        if RECORD_VIDEO in worklist:
            self.mov_rec.save_frame(wxbmp)
            
        if DISPLAY_INDEPENDENT_VIDEO in worklist:
            self.video_window.update_image(wximg, self.UAVinfo.get_information_in_InfoEntries())
        
       
        # 结束图像传输需要先停止track
        if DISPLAY_TRACK_VIDEO in worklist:       
            memtrack = wx.MemoryDC()
            #图像滤波
            
            self.cambuf.append(srcimg)
            self.cambuf.pop(0)
            a=time.clock()
            srcimg = img_filter(self.cambuf)
#             print '%.6f'%((time.clock()-a)*1000)

#             self.cambuf.append(srcimg)
#             self.cambuf.pop(0)
            
            
            # 显示原始图像
            if self.display_track_state == DISPLAY_TRACK_STATE_RAW:
                #rstimg = self.get_adjusted_image(srcimg)
                rstimg = srcimg
                rstbmp = util.cvimg_to_wxbmp(rstimg)           
            # 正在框选状态
            elif self.display_track_state == DISPLAY_TRACK_STATE_SELECTION:
                assert self.frozen_frame is not None, 'Frozen frame is none.'
                rectimg = self.get_dragging_image(self.frozen_frame,self.drag_info.get_drag_data())
                rstbmp = util.cvimg_to_wxbmp(rectimg)
            # 显示目标追踪结果
            elif self.display_track_state == DISPLAY_TRACK_STATE_RESULT:
                track_mode = self.m_choice_track_mode.GetStringSelection()
                display_process = self.m_menuItem_track_display_process.IsChecked()
                if track_mode == 'template':
                    method = METHOD.TEMPLATEMATCH
                elif track_mode == 'meanshift':
                    method = METHOD.MEANSHIFT
                elif track_mode == 'gray-meanshift':
                    method = METHOD.GRAYMEANSHIFT
                else:
                    method = METHOD.OPTICALFLOW
                
                matchimg, center, res = self.objmatch.process(method, srcimg)
                if display_process:
                    rstbmp = util.cvimg_to_wxbmp(res)
                    tmpimg = res
                else:
                    rstbmp = util.cvimg_to_wxbmp(matchimg)
                    tmpimg = matchimg
            
                if TRACK_OBJECT in worklist:
                    self.trackctrl.add_pt(center)
                
            
            # TODO:MeanShift-OpticalFlow 卡尔曼
                
            # 更新track bitmap 界面
            memtrack.SelectObject(rstbmp)
            memtrack.SetUserScale(float(srcimg.shape[1])/float(self.bitmap_track_size[0]),
                             float(srcimg.shape[0])/float(self.bitmap_track_size[1]))
            self.dc_track.Blit(0, 0, self.bitmap_track_size[0], self.bitmap_track_size[1], memtrack, 0, 0)
            a = time.clock()
        
        # 5 Hz Tasks
        if (time.clock()-self.timer.last_time) > (1.0/TASK_LOW_FREQ):
            self.timer.last_time=time.clock()
            
            
            if DISPLAY_XBEE_DATA in worklist:
                self.update_rcv_area()
            
            if USING_JOYSTICK in self.worklist:
                self.do_joy_control()
            # 发送MID=0x09时自动返回，不需重复发送。
            elif DISPLAY_UAVINFO in self.worklist:
                self.send_data_by_frame(MsgPrcs.pack_control(0, self.state_smart_direction))
            
            if DISPLAY_UAVINFO in self.worklist:
                self.update_GUI_UAVinfo(self.UAVinfo.get(-2))
        
            if TRACK_OBJECT in worklist:
                now_height = self.UAVinfo.get().height
                self.trackctrl.update_h(3 if math.isnan(now_height) else now_height)
                flowspeedx=self.UAVinfo.get(-2).rposx
                flowspeedy=self.UAVinfo.get(-2).rposy
                du = self.trackctrl.get_u(flowspeedx,flowspeedy)
                
                rstimg = self.objmatch.draw_circles(tmpimg, self.trackctrl.pts[-1], color='GREEN', radius=10)
                rstbmp = util.cvimg_to_wxbmp(rstimg)
                memtrack.SelectObject(rstbmp)
                memtrack.SetUserScale(float(srcimg.shape[1])/float(self.bitmap_track_size[0]),
                                 float(srcimg.shape[0])/float(self.bitmap_track_size[1]))
                self.dc_track.Blit(0, 0, self.bitmap_track_size[0], self.bitmap_track_size[1], memtrack, 0, 0)
                
                self.send_ref(du)
        
        n = time.clock()
#         print('[work time]%4.4f [cir time]%4.4f'%((n-a)*1000,(n-self.lasttime)*1000))
        self.lasttime = n
    
#------ Tool Function ------       
    def send_ref(self,u):
        x,y,z = u
        h=0
        rtn = self.send_data_by_frame(MsgPrcs.pack_ref(x,y,z,h))
#         self.sbar.update(u'给定<%.4f,%.4f,%.4f,%.4f>已发送(%d)'%(x,y,z,h,rtn))
        self.sbar.update(u'给定<r=%.4f,p=%.4f,y=%.4f>已发送(%d)'%(x,y,z,rtn))
    
    def update_GUI_UAVinfo(self, info):
        # update text info
        mem = wx.MemoryDC()
        mem.SetFont(util.WXFONT)
        
        csz = mem.GetTextExtent(' ')
        sz = (45*csz[0], 10*csz[1])
        
        self.m_bitmap_uavinfo.SetSize(sz)
        self.m_bitmap_uavinfo.CenterOnParent()
        mem.SelectObject(wx.BitmapFromImage(wx.ImageFromData(sz[0],sz[1],'\xf0'*sz[0]*sz[1]*3)))
        
        pos = (0,5)
        padding = csz[0]*4
        
        def write(s, color=None):
            if color is None:
                color = wx.BLUE
            mem.SetTextForeground(color)
            mem.DrawText(s, pos[0], pos[1])
            return (pos[0] + mem.GetTextExtent(s)[0] + padding, pos[1])
        
        def writeln(s, color=None):
            rtn =  write(s, color)
            return (0, rtn[1]+csz[1])
            
        def get_st_color(value):
            if value == 0:
                return wx.Colour(255,0,0)
            elif value == 2:
                return wx.Colour(255,255,0)
            elif value == 1:
                return wx.Colour(20,215,0)
            else:
                return wx.Colour(160,160,160)
        
        pos = writeln('--UAVInfo Display--    UAVTime :%9.3Fs'%info.uavtime)
        pos = writeln('', None)
        pos = writeln(' pitch  =%9.3Fd    Rpitch  =%9.3Fd'%(info.pitch, info.ref_pitch))
        pos = writeln(' roll   =%9.3Fd    Rroll   =%9.3Fd'%(info.roll, info.ref_roll))
        pos = writeln(' yaw    =%9.3Fd    Ryaw    =%9.3Fd'%(info.yaw, info.ref_yaw))
        pos = write(' height =%9.3Fm'%info.height,
                    wx.RED if self.UAVinfo.need_warning('height', info.height) else None)
        pos = writeln('Rheight =%9.3Fm\n'%(info.ref_height))
        pos = write(' volt   =%9.3FV'%info.volt,
                    wx.RED if self.UAVinfo.need_warning('volt', info.volt) else None)
        pos = writeln('Rthrust =%9.3F'%(info.ref_thrust))
        pos = writeln(' Pos(%5.2f,%5.2f)  Rpos(%5.2f,%5.2f)'%(info.posx,info.posy,info.rposx,info.rposy))
        pos = write(' JOY', get_st_color(info.st_ct))
        pos = write('MOTOR', get_st_color(info.st_mt))
        pos = write('AutoHeight', get_st_color(info.st_ah))
        pos = write('Smart Dir.', get_st_color(info.st_sd))

        self.dc_uavinfo.Blit(0, 0, sz[0],sz[1], mem, 0, 0)
        
        # update bitmap_atti
        attiimg = self.UAVinfo.get_attitude_img(info.pitch, info.roll, info.yaw)
        self.dc_attitude.DrawBitmap(util.cvimg_to_wxbmp(attiimg), 0, 0)        
    
    def update_GE(self, info):
        la = info.la
        lo = info.lo
        if self.GE_uninited:
            js = util.JSCODESINIT%(la,lo, info.height*1.2)
            self.GE_uninited = False
        else:
            js = util.JSCODES%(la,lo, info.height*1.2)
        self.browser_ge.RunScript(js)
    
    def get_hist_channel(self):
        if self.m_menuItem_track_hist_h.IsChecked():
            return [0]
        elif self.m_menuItem_track_hist_s.IsChecked():
            return [1]
        elif self.m_menuItem_track_hist_l.IsChecked():
            return [2]
    
    def enable_video_components(self, switch):
        for each in [self.m_button_video_window_show, 
                     self.m_bitmap_video,
                     self.m_button_record,
                     self.m_filePicker_output
                     ]:
            each.Enable(switch)  
        self.m_button_record.Enable(False)         
    
    def OnClose(self, event):
        print('Close window...')
        self.timer.Stop()
#         try:
#             self.camcap.release()
#         except AttributeError:
#             print('No camcap, release failed.')
        if self.m_button_toggle_xbee.is_running:
            self.close_xbee(self.m_button_toggle_xbee)
        if self.m_button_toggle_track_video.is_running:
            self.close_video(self.m_button_toggle_track_video)
        self.Destroy()

class App(wx.App):
    
    def OnInit(self):
        self.frame = GroundStation()
        self.frame.Show()
        self.SetTopWindow(self.frame)
        
        return True
    
    def OnExit(self):
        print('Exit APP...')
        
        
if __name__ == '__main__':
    app = App(redirect=False)
    util.init_font()
    app.MainLoop()
