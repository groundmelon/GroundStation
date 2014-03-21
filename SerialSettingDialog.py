# -*- coding: utf-8 -*- 

'''
Created on 2013-12-4

@author: Administrator
'''
import wx
from GroundStationBase import frame_serial_setting
from communication.XBeeComm import XBee
import serial.tools.list_ports as lstprt

class SerialSetting(frame_serial_setting):
    def __init__(self,parent, option_arg = None):
        frame_serial_setting.__init__(self,parent)
        self.comm = parent.comm
        serial_info = self.comm.get_supported_info()
        
        self.parity_table = {}
        for s in serial_info['parity']:
            self.parity_table[s[0]] = s
        
        self.stopbit_table = {}
        for s in serial_info['stopbit']:
            self.stopbit_table[float(s)] = s
        
        self.init_options(serial_info)
        if option_arg is None:
            option = {'com'     :   serial_info['com'][0],
                      'baudrate':   9600,
                      'bytesize':   8,
                      'parity'  :   'None',
                      'stopbit' :   1,
                      'RtsCts':False,#hard flow control
                      'XonXoff':False,#software flow control
                      }
        else:
            option = option_arg
        self.set_options(option)
        
       
    def on_see_com_info(self, event):
        wx.MessageBox(self.comm.get_com_info(), u"串口信息",wx.OK | wx.ICON_INFORMATION)
    
    def get_options(self):
        option = {'com'     :   self.m_choice_com.GetStringSelection(),
                  'baudrate':   int(self.m_choice_baudrate.GetStringSelection()),
                  'bytesize':   int(self.m_choice_bytesize.GetStringSelection()),
                  'parity'  :   self.m_choice_parity.GetStringSelection()[0],
                  'stopbit' :   float(self.m_choice_stopbit.GetStringSelection()),
                  'RtsCts':self.m_checkBox_RtsCts.IsChecked(),
                  'XonXoff':self.m_checkBox_XonXoff.IsChecked(),
                  }
        return option

    def set_options(self,option):
        self.m_choice_com.      SetStringSelection(str(option['com']))
        self.m_choice_baudrate. SetStringSelection(str(option['baudrate']))              
        self.m_choice_bytesize. SetStringSelection(str(option['bytesize']))
        self.m_choice_stopbit.  SetStringSelection(self.stopbit_table[option['stopbit']])
        self.m_choice_parity.   SetStringSelection(self.parity_table[option['parity']])
        self.m_checkBox_RtsCts. SetValue(option['RtsCts'])
        self.m_checkBox_XonXoff.SetValue(option['XonXoff'])        
        
        
        
    def init_options(self,info):      
        self.m_choice_com.SetItems([each[0] for each in lstprt.comports()])
        self.m_choice_baudrate.SetItems(info['baudrate'])
        self.m_choice_bytesize.SetItems(info['bytesize'])
        self.m_choice_parity.SetItems(info['parity'])
        self.m_choice_stopbit.SetItems(info['stopbit'])
