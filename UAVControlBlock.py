# -*- coding: utf-8 -*- 
'''
Created on 2014-4-1

@author: GroundMelon
'''
import communication.MessageProcess as MsgPrcs
from JoyController import JoyCtrl
import util
from Definition import USING_JOYSTICK
import wx

class UAVCtrlBlock():
    def send_pt_reference(self):
        pitch = float(self.m_spinCtrl_PT_pitch.GetValue())
        roll = float(self.m_spinCtrl_PT_roll.GetValue())
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
    
    def update_joy_status(self):
        s = 'Joystick ON\n\n'
        rtn = self.joy.get_axis()
        s += ''.join(['%s:%4d\n'%(k.rjust(8,' '),v) for k,v in rtn.iteritems()])
        rtn = self.joy.get_button()
        s += ''.join(['%s:%4d\n'%(('btn%2d'%(i+1)).rjust(8,' '),rtn[str(i+1)]) for i in range(12)])
        s += '%s:%s'%('hat'.rjust(8),str(self.joy.get_hat()))
        
        self.m_staticText_joystick.SetLabel(s)
    
    def toggle_smart_direction(self, switch):
        return self.send_data_by_frame(MsgPrcs.pack_smart_direction(switch))
        