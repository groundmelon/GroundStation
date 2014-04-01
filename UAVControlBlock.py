# -*- coding: utf-8 -*- 
'''
Created on 2014-4-1

@author: GroundMelon
'''
import communication.MessageProcess as MsgPrcs

class UAVCtrlBlock():
    def send_pt_reference(self):
        pitch = float(self.m_spinCtrl_PT_pitch.GetValue())
        roll = float(self.m_spinCtrl_PT_roll.GetValue())
        return self.send_data_by_frame(MsgPrcs.pack_pt(p=pitch, r=roll))