# -*- coding: utf-8 -*- 
'''
Created on 2014-2-18

@author: GroundMelon
'''
from binascii import b2a_hex
import wx
import util

class CommBlock():
    def send_data_by_GUI(self):
        gui_data = self.m_textCtrl_comm_send.GetValue().encode('ascii','ignore')
        self.history.add(gui_data)
        
        if self.m_choice_send_style.GetStringSelection() == 'HEX':          
            rtn = self.send_data_by_frame(''.join([chr(int(x,16)) for x in gui_data.split()]))
        elif self.m_choice_send_style.GetStringSelection() == 'ASCII':
            rtn = self.send_data_by_frame(gui_data)
        else:
            assert False, u'Send type is not ASCII nor HEX!'
            return
        if self.m_checkBox_sent_clear.IsChecked():
            self.m_textCtrl_comm_send.SetValue('')
        self.sbar.update(u'本次发送%d字节'%rtn)
    
    def send_data_by_frame(self, data):
        rtn = self.comm.send_string(data)
        
    def get_command(self):
        data = self.comm.get_rcvbuf()
        #print(''.join(data))
        '''example (H099.9 P+45.0 R+30.0 Y+40.0 V11.2 A+045.732433 O+126.628802) 
                   1098765432109876543210987654321098765432109876543210987654321
                   6         5         4         3         2         1         0
        '''
        if len(data)>= 61 and '(' == data[-61] and ')' == data[-1]:
            s = ''.join(data[-61:])
            return (float(s[-59:-54]),
                    float(s[-52:-47]),
                    float(s[-45:-40]),
                    float(s[-38:-33]),
                    float(s[-31:-27]),
                    float(s[-25:-14]),
                    float(s[-12:-1]),
                    )
        else:
            return None
    
    
    
    def update_rcv_area(self):
        data = self.comm.get_rcvbuf()
        if self.m_choice_recv_style.GetStringSelection() == 'HEX':
            s = ' '.join([b2a_hex(x) for x in data]).upper()
        elif self.m_choice_recv_style.GetStringSelection() == 'ASCII':
            s = ''.join([x for x in data])
        else:
            assert False, u'Send type is not ASCII nor HEX!'
            return
        self.m_textCtrl_comm_receive.SetValue('')
        self.m_textCtrl_comm_receive.AppendText(s)
    
    def enable_comm_components(self, switch):
        self.m_panel_comm.Enable(switch)
        for each in self.m_panel_comm.GetChildren():
            each.Enable(switch)
        
        self.m_panel_para_adj.Enable(switch)
        for each in self.m_panel_para_adj.GetChildren():
            each.Enable(switch)
    
class InputHistory(object):
    def __init__(self,window):
        self.window = window
        self.history=[]
        self.cursor = -1
    
    def clear(self):
        self.history=[]
        self.cursor = -1
        
    def add(self,s):
        self.history.append(s)
        self.cursor = len(self.history)    
    
    def getByRel(self,rel):
        ret = ""
        try:
            
            if self.cursor+rel == -1:
                ret = self.history[0]
                raise IndexError
            if self.cursor+rel == len(self.history):
                ret = self.history[self.cursor]
                raise IndexError                        
            ret = self.history[self.cursor+rel]
            self.cursor = self.cursor+rel
            self.window.SetStatusText("历史记录[%d]:%s"%(self.cursor+1,ret),0)
        except IndexError:
            self.window.SetStatusText("没有更多历史记录",0)
        return ret
    
    def getByAbs(self,cur):
        try:
            if cur == -1:
                raise IndexError
            ret = self.history[cur]
            self.window.SetStatusText("历史记录:%s"%ret,0)
        except IndexError:
            self.window.setStatusText("没有更多历史记录",0)
            ret = ""
        return ret