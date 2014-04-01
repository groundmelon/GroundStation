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

import util
import os
import wx
import wx.html2
import time

from Definition import *
from imageprocess.ObjectTracking import get_adjusted_image


class GroundStation(FrameGroundStationBase, WorkBlock ,TrackBlock, VideoBlock,
                    ButtonBlock, MenuBlock, CommBlock, ParameterAdjustBlock,
                    UAVCtrlBlock
                    ):
    def __init__(self):
        self.lasttime = time.clock()
        super(GroundStation, self).__init__(parent = None)
        self.SetIcon(wx.Icon(r'resources/gs.ico', wx.BITMAP_TYPE_ICO))              
        
        #---- init status bar system ----
        self.sbar = StatusBarSystem(self.m_statusBar)
        
        #---- add Google Earth Components ----  
        sizer_ge = self.m_panel_route.GetSizer()
        self.browser_ge = wx.html2.WebView.New(self.m_panel_route, size=(330,330))
        sizer_ge.Add(self.browser_ge, 1, wx.ALIGN_CENTER, 0)
        self.browser_ge.LoadURL(r'file:///%s/resources/ge.html'%os.getcwd().replace('\\','/'))
        self.GE_uninited = True
        
        #---- add uavinfo menuItem ----
        
        #---- set record labels ----
        self.m_filePicker_output.GetPickerCtrl().SetLabel(u'设置视频参数')
        
        #---- add component attributes ----
        for comp in [self.m_button_toggle_track, 
                     self.m_button_toggle_track_video,
                     self.m_button_toggle_video,
                     self.m_button_toggle_xbee,
                     self.m_button_update_uavinfo,
                     self.m_button_select_object,
                     self.m_button_toggle_track,
                     self.m_button_record,
                     ]:
            comp.__setattr__('is_running', False)

        #---- init comm block ----
        self.comm = XBee(self)
        self.comm_options = {}
        self.load_default_comm_options()
        self.history = InputHistory(self)
        self.enable_comm_relative_components(False)
        #self.xbee_comm_state = False
        #self.init_track_bitmap()
        #wx.InitAllImageHandlers()
        
        #---- init video block ----
        self.cap_dev_num = 0
        self.enable_video_components(False)
        #self.video_on = False
        self.video_window = None
        
        #---- init track block ----
        self.enable_track_components(False)
        self.display_track_state = None
        #self.track_video_on = False
        #self.track_on = False
        
        #---- init para adj block ----
        self.init_para_block()
        
        #---- init information variables ----
        self.bitmap_track_size = tuple(self.m_bitmap_track.GetSize())
        self.bitmap_video_size = tuple(self.m_bitmap_video.GetSize())
        
        #---- init UAVInformation ----
        self.UAVinfo = UAVInfomation()
        
        
        
        # --- dc init ---
        self.dc_video = wx.ClientDC(self.m_bitmap_video)
        self.dc_track = wx.ClientDC(self.m_bitmap_track)
        self.memory = wx.MemoryDC()
        self.dc_attitude = wx.ClientDC(self.m_bitmap_attitude)
        # --- test ---
        self.multimean_arg = None
        self.edge_arg = None
        
        self.init_worklist()
        #self.Bind(wx.EVT_IDLE, self.main_work)
        self.timer = wx.Timer(self)
        self.Bind(wx.EVT_TIMER, self.main_work, self.timer)
        self.timer.Start(1000/20)
        
        self.timer1 = wx.Timer(self) 
        self.Bind(wx.EVT_TIMER, self.main_work1, self.timer1)
        self.timer1.Start(1000/10)
        
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
        self.UAVinfo.save_to_file(self, pidpara = self.get_para_from_table())
        if self.m_menuItem_clear_uav_info_after_save.IsChecked():
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

# 跟踪画面在独立窗口中显示功能暂时屏蔽
#     def on_track_image_show(self, event):
#         self.track_imshow_window = self.create_image_show_window()
     
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
                        )
                       )
    
    def on_load_para(self, event):
        self.load_para()
    
    def on_save_para(self, event):
        self.save_para()
    
    def on_set_down_para(self, event):
        self.set_down_para()

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
#             self.UAVinfo.update(data[0], data[1], data[2], data[3], data[4], data[5], data[6])
#             attiimg = self.UAVinfo.get_attitude_img()
#             self.dc_attitude.DrawBitmap(util.cvimg_to_wxbmp(attiimg), 0, 0)
#             self.update_GUI_UAVinfo(self.UAVinfo.get())
#             self.update_GE(self.UAVinfo.get())
    
#     def on_update_track_bitmap(self,bmp):
#         self.dc_track.DrawBitmap(bmp, 0, 0)
#         #self.m_bitmap_track.SetBitmap(bmp)
#       
#     def on_timer_update_track_bitmap(self, event):
#         self.st.next()
#         self.update_track_bitmap(self.st.get_source())
#     
#     def update_attitude_bitmap(self):
#         rtnval = self.attidisp.test()
#         self.m_bitmap_attitude.SetBitmap(wx.BitmapFromBuffer(rtnval[0], rtnval[1], rtnval[2]))
    
#------ Work Function ------        
    def main_work(self, event):
        worklist = self.worklist
        a = time.clock()        
        
        if DISPLAY_XBEE_DATA in worklist:
            self.update_rcv_area()
#         if DISPLAY_UAVINFO in worklist:
#             self.send_data_by_frame(MsgPrcs.pack_get_info())
        
        if DISPLAY_VIDEO in worklist:
            srcimg = self.camcap.get_frame()
            wxbmp = util.cvimg_to_wxbmp(srcimg)
            memvideo = wx.MemoryDC()
            memvideo.SelectObject(wxbmp)

            if self.m_menuItem_video_osd.IsChecked():
                # draw time
                memvideo.SetTextForeground( wx.BLUE )
                memvideo.SetFont( util.WXFONT )
                pos = (srcimg.shape[1] - util.PADDING - util.TIME_TEXT_WIDTH, util.PADDING)
                #pos = (self.bitmap_video_size[0] - util.PADDING - util.TIME_TEXT_WIDTH, util.PADDING)
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
            self.video_window.update_image_with_info(srcimg, self.UAVinfo.get_information_in_InfoEntries())
        # 结束图像传输需要先停止track
        if DISPLAY_TRACK_VIDEO in worklist:       
            memtrack = wx.MemoryDC()
            # 显示原始图像
            if self.display_track_state == DISPLAY_TRACK_STATE_RAW:
                rstimg = self.get_adjusted_image(srcimg)
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
                # 模板匹配模式
                if track_mode == 'template':
                    matchimg, center, res = self.objmatch.do_tpl_match(srcimg)
                    if display_process:
                        rstbmp = util.cvimg_to_wxbmp(res)
                    else:
                        #rszimg = util.cvimg_resize(matchimg, self.bitmap_track_size)
                        rstbmp = util.cvimg_to_wxbmp(matchimg)
                # 边缘检测-模板匹配模式
                elif track_mode == 'edge-tpl':
                    matchimg, center, edgeimg = self.objmatch.do_edge_match(srcimg,self.edge_arg)
                    if display_process:
                        rstbmp = util.cvimg_to_wxbmp(edgeimg)
                    else:
                        rstbmp = util.cvimg_to_wxbmp(matchimg)
                # 纯色匹配模式
                elif track_mode == 'color':
                    matchimg, center, mask = self.objmatch.do_color_match(srcimg)
                    if display_process:
                        rstbmp = util.cvimg_to_wxbmp(mask)
                    else:
                        rstbmp = util.cvimg_to_wxbmp(matchimg)
                # MeanShift匹配模式
                elif track_mode == 'meanshift':
                    matchimg, center, prj_img = self.objmatch.do_meanshift(srcimg)
                    if display_process:
                        rstbmp = util.cvimg_to_wxbmp(prj_img)
                    else:
                        rstbmp = util.cvimg_to_wxbmp(matchimg)
                # 多目标MeanShift匹配模式
                elif track_mode == 'multi-meanshift':
                    matchimg, center, prj_img = self.objmatch.do_multi_meanshift(srcimg, self.multimean_arg)
                    if display_process:
                        rstbmp = util.cvimg_to_wxbmp(prj_img)
                    else:
                        rstbmp = util.cvimg_to_wxbmp(matchimg)
                # 混合匹配模式
                elif track_mode == 'mix':
                    matchimg, center, _ = self.objmatch.do_mix(srcimg, self.multimean_arg, self.edge_arg)    
                    rstbmp = util.cvimg_to_wxbmp(matchimg)
            # 更新track bitmap 界面
            memtrack.SelectObject(rstbmp)
            memtrack.SetUserScale(float(srcimg.shape[1])/float(self.bitmap_track_size[0]),
                             float(srcimg.shape[0])/float(self.bitmap_track_size[1]))
            self.dc_track.Blit(0, 0, self.bitmap_track_size[0], self.bitmap_track_size[1], memtrack, 0, 0)
                
        
        if TRACK_OBJECT in worklist:
            print('tracking')
        n = time.clock()
        #print('[work time]%4.4f [cir time]%4.4f'%((n-a)*1000,(n-self.lasttime)*1000))
        self.lasttime = n
    
    def main_work1(self, event):
        if DISPLAY_UAVINFO in self.worklist:
            self.send_data_by_frame(MsgPrcs.pack_get_info())
            self.update_GUI_UAVinfo(self.UAVinfo.get())
            
#------ Tool Function ------       
    def update_GUI_UAVinfo(self, info):
        # update text info
        for k,v in info.iteritems():
            if v is None:
                info[k] = float('nan')
        s =  '---UAV Info Display---\tUAVTime : %.3Fs\n\n'%info['uavtime']
        s += ' pitch  =%9.3Fd\tRpitch  =%9.3Fd\n'%(info['pitch'], info['ref_pitch'])
        s += ' roll   =%9.3Fd\tRroll   =%9.3Fd\n'%(info['roll'], info['ref_roll'])
        s += ' yaw    =%9.3Fd\tRyaw    =%9.3Fd\n'%(info['yaw'], info['ref_yaw'])
        
        s_war = '*' if self.UAVinfo.need_warning('height', info['height']) else ' '
        s += '%sheight =%9.3Fm\tRheight =%9.3Fm\n'%(s_war, info['height'],info['ref_height'])
        
        s_war = '*' if self.UAVinfo.need_warning('volt', info['volt']) else ' '
        s += '%svolt   =%9.3FV\tRthrust =%9.3F \n'%(s_war, info['volt'], info['ref_thrust'])
        
        self.m_textCtrl_info.ChangeValue(s)
        
        # update image info
        attiimg = self.UAVinfo.get_attitude_img()
        self.dc_attitude.DrawBitmap(util.cvimg_to_wxbmp(attiimg), 0, 0)
#         self.m_staticText_height.SetLabel('%.4fm'%info['height'])
#         if self.UAVinfo.need_warning('height', info['height']):
#             self.m_staticText_height.SetForegroundColour((255,0,0))
#         else:
#             self.m_staticText_height.SetForegroundColour((0,0,0))
#         
#         self.m_staticText_vol.SetLabel('%.4fv'%info['vol'])
#         if self.UAVinfo.need_warning('vol', info['vol']):
#             self.m_staticText_vol.SetForegroundColour((255,0,0))
#         else:
#             self.m_staticText_vol.SetForegroundColour((0,0,0))
#         
#         self.m_staticText_pitch.SetLabel('%.4fd'%info['pitch'])
#         self.m_staticText_roll.SetLabel('%.4fd'%info['roll'])
#         self.m_staticText_yaw.SetLabel('%.4fd'%info['yaw'])
    
    def update_GE(self, info):
        la = info['la']
        lo = info['lo']
        if self.GE_uninited:
            js = util.JSCODESINIT%(la,lo, info['height']*1.2)
            self.GE_uninited = False
        else:
            js = util.JSCODES%(la,lo, info['height']*1.2)
        self.browser_ge.RunScript(js)
    
    def set_track_arg(self, s):
        sel = self.m_choice_track_arg.GetStringSelection()
        if 'multi' == sel:
            self.multimean_arg = float(s)
        elif 'edge' == sel:
            self.edge_arg = float(s)
    
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
        #self.Bind(wx.EVT_IDLE, None)
        self.timer.Stop()
        try:
            self.camcap.release()
        except AttributeError:
            print('No camcap, release failed.')
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
