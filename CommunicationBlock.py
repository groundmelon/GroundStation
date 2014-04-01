# -*- coding: utf-8 -*- 
'''
Created on 2014-2-18

@author: GroundMelon
'''
from binascii import b2a_hex
import wx
import util
import communication.MessageProcess as MsgPrcs
import PickleFileIO

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
        return self.comm.send_string(data)
        
    def get_backdata(self):
        buf = self.comm.get_rcvbuf()
        '''
                        更新位姿高度电压： FF 04 00 00 80 3F 00 00 00 40 00 00 40 40 00 40 1C 46 00 00 A0 40 AA
                        更新经纬坐标：        FF 0F 10 EE 36 42 BC 41 FD 42 00 00 00 00 00 00 00 00 00 00 00 00 AA
        '''
        if len(buf)>=23:
            return MsgPrcs.unpack(''.join(buf[-23:]))
        else:
            return (None, None)
    
    
    
    def update_rcv_area(self, refresh = False):
        if refresh:
            data = self.comm.get_rcvbuf()
            func = 'ChangeValue'
        else:
            data = self.comm.get_new_buf()
            func = 'AppendText'
        if data:
            if self.m_choice_recv_style.GetStringSelection() == 'HEX':
                s = ' '.join([b2a_hex(x) for x in data]).upper()+' '
            elif self.m_choice_recv_style.GetStringSelection() == 'ASCII':
                s = ''.join([x if x<'\xF0' else ' ' for x in data])
            else:
                assert False, u'Send type is not ASCII nor HEX!'
                return
        else:
            s = ''
        #eval("self.m_textCtrl_comm_receive.%s"%func)('%s'%s.__repr__()[1:-1])
        eval("self.m_textCtrl_comm_receive.%s"%func)(s)
    
    def process_backdata(self, msgtype, data):
        for (k,v) in MsgPrcs.PKGTYPE_PID.iteritems():
            if v == msgtype:
                self.update_rcv_pid(k, data[:4])
                return True
        if msgtype == MsgPrcs.PKGTYPE_INFO:
            self.UAVinfo.update_info(data[0], data[1], data[2], data[3], data[4])
        
        elif msgtype == MsgPrcs.PKGTYPE_LOC:
            self.UAVinfo.update(None, None, None, None, None, data[0], data[1])
            self.update_GE(self.UAVinfo.get())
        
        elif msgtype == MsgPrcs.PKGTYPE_REF:
            self.UAVinfo.update_ref(data[0], data[1], data[2], data[3], data[4])
        
        elif msgtype == MsgPrcs.PKGTYPE_U0:
            self.UAVinfo.update_u0(data[0], data[1], data[2], data[3], data[4])
        
        elif msgtype == MsgPrcs.PKGTYPE_U1:
            self.UAVinfo.update_u1(data[0], data[1], data[2], data[3], data[4])
            
    def enable_comm_relative_components(self, switch):
        #self.m_panel_comm.Enable(switch)
        for each in self.m_panel_comm.GetChildren():
            if each != self.m_textCtrl_comm_receive:
                each.Enable(switch)
        
        #self.m_panel_para_adj.Enable(switch)
        for each in self.m_panel_para_adj.GetChildren():
            each.Enable(switch)
        
        self.m_button_update_uavinfo.Enable(switch)
        
        #self.m_panel_uavctrl.Enable(switch)
        for each in self.m_panel_uavctrl.GetChildren():
            each.Enable(switch)
    
    def load_default_comm_options(self):
        # load default settings
        filepath = r'communication\xbee.gss'
        try:
            pfio = PickleFileIO.PickleFileIO(filepath)
            self.comm_options = pfio.load()
            self.sbar.update(u'默认通信设置"%s"已经应用。'%filepath)
        except (EOFError,IOError),e:
            self.m_statusBar.SetStatusText(u'未发现默认设置')
    
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