# -*- coding: utf-8 -*- 
'''
Created on 2014-4-1

@author: GroundMelon
'''
from GroundStationBase import FrameGroundStationBase
import communication.MessageProcess as MsgPrcs
from JoyController import JoyCtrl
import util
from Definition import USING_JOYSTICK,CAMERA_PT_PITCH
import wx

class UAVCtrlBlock(FrameGroundStationBase, object):
    def init_uav_control(self):
        self.state_smart_direction = False
        self.camera_pt_pitch = CAMERA_PT_PITCH
        self.m_spinCtrl_PT_pitch.SetValue(self.camera_pt_pitch)
    
    def send_pt_reference(self):
        pitch = float(self.m_spinCtrl_PT_pitch.GetValue())
        roll = float(self.m_spinCtrl_PT_roll.GetValue())
        self.camera_pt_pitch = pitch
        return self.send_data_by_frame(MsgPrcs.pack_pt(p=pitch, r=roll))
    
    def open_joystick(self, comp):
        try:
            self.joy = JoyCtrl()
            util.toggle_button(comp, u'开启', u'关闭')
            self.add_work(USING_JOYSTICK)
        except AssertionError,e:
            if e.args[0] is 'NOJOYSTICK':
                wx.MessageBox(u"未找到摇杆", u"出现错误",wx.OK | wx.ICON_ERROR)
            else:
                raise AssertionError, e
    def close_joystick(self, comp):
        self.remove_work(USING_JOYSTICK)
        self.joy.release()
        self.m_staticText_joystick.SetLabel('Joystick OFF')
        util.toggle_button(comp, u'开启', u'关闭')
    
    
    def do_joy_control(self):
        rst = self.joy.get_ctrl()
        p = rst['pitch']
        r = rst['roll']
        y = rst['yaw']
        t = rst['throttle']
        ctrltype = rst['ctrltype']
        sd = rst['sd']
        
        self.state_smart_direction = bool(sd)
        self.m_checkBox_smart_direction.SetValue(self.state_smart_direction)
        
        self.update_joy_status(rst)
        return self.send_data_by_frame(MsgPrcs.pack_control(ctrltype,sd,p,r,y,t))
        
    
    def update_joy_status(self, rst=None):
        if rst is None:
            rst = self.joy.get_ctrl()
        s = 'Joystick ON\n\n'
        s += ''.join(['%s:%4d\n'%(k.rjust(8,' '),v) for k,v in rst.iteritems()])
#         rtn = self.joy.get_button()
#         s += ''.join(['%s:%4d\n'%(('btn%2d'%(i+1)).rjust(8,' '),rtn[i]) for i in range(12)])
#         s += '%s:%s\n'%('t'.rjust(8),self.joy.get_hat()*250+1500)
#         s += 'ctrltype %d\n'%rtn['ctrltype']
        
        
        self.m_staticText_joystick.SetLabel(s)
    
    def toggle_smart_direction(self, switch):
        self.state_smart_direction = switch
        