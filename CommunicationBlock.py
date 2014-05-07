# -*- coding: utf-8 -*- 
'''
通信功能区
Created on 2014-2-18

@author: GroundMelon
'''
from binascii import b2a_hex
import wx
import util
import communication.MessageProcess as MsgPrcs
import PickleFileIO
from GroundStationBase import FrameGroundStationBase

class CommBlock(FrameGroundStationBase,object):
    '''
    通信功能区
    
    包含一些与GUI相关的，与通信相关的函数
    '''
    def send_data_by_GUI(self):
        '''
        在GUI端触发了数据发送功能的执行函数，从Text Area里获得发送数据
        '''
        gui_data = self.m_textCtrl_comm_send.GetValue().encode('ascii','ignore')
        self.history.add(gui_data)
        
        # text area中的内容是hex/ascii格式分别处理
        if self.m_choice_send_style.GetStringSelection() == 'HEX':          
            # 按空格分离，str->int->char，把hexstring转为byte-string
            rtn = self.send_data_by_frame(''.join([chr(int(x,16)) for x in gui_data.split()]))
        elif self.m_choice_send_style.GetStringSelection() == 'ASCII':
            # 直接发送
            rtn = self.send_data_by_frame(gui_data)
        else:
            assert False, u'Send type is not ASCII nor HEX!'
            return
        if self.m_checkBox_sent_clear.IsChecked():
            # 发送后清空
            self.m_textCtrl_comm_send.SetValue('')
        self.sbar.update(u'本次发送%d字节'%rtn)
    
    def send_data_by_frame(self, data):
        '''
        直接由frame发送数据，比如控制指令，不需读取text area 的值
        @param data: 待发送数据，string
        @return: 发送的字节数
        '''
        return self.comm.send_string(data)
        
    def get_backdata(self):
        '''
        从通信模块获取传回的数据
        @return: 数据有效，返回值参考L{GroundStation.communication.MessageProcess.unpack_type}，数据无效为(None,None)
        '''
        buf = self.comm.get_rcvbuf()

        if len(buf)>=23:
            tmp=buf[-23::]
            return MsgPrcs.unpack_type(''.join(buf[-23::]))
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
        eval("self.m_textCtrl_comm_receive.%s"%func)(s)
    
    def process_backdata(self, msgtype, buf):
        for (k,v) in MsgPrcs.PKGTYPE_PID.iteritems():
            if v == msgtype:
                data = MsgPrcs.unpack_5f(buf)
                self.update_rcv_pid(k, data[:4])
                return True
        if msgtype == MsgPrcs.PKGTYPE_ATTI:
            data = MsgPrcs.unpack_5f(buf)
            self.UAVinfo.update_info(data)
        
        elif msgtype == MsgPrcs.PKGTYPE_LOC:
            data = MsgPrcs.unpack_5f(buf)
            self.UAVinfo.update(None, None, None, None, None, data[0], data[1])
            self.update_GE(self.UAVinfo.get())
        
        elif msgtype == MsgPrcs.PKGTYPE_REF:
            data = MsgPrcs.unpack_5f(buf)
            self.UAVinfo.update_ref(data)
        
        elif msgtype == MsgPrcs.PKGTYPE_CTRL:
            data = MsgPrcs.unpack_ctrl(buf)
            self.UAVinfo.update_status(data)
        
        elif msgtype == MsgPrcs.PKGTYPE_POS:
            data = MsgPrcs.unpack_5f(buf)
            self.UAVinfo.update_pos(data)
        
        elif msgtype == MsgPrcs.PKGTYPE_U0:
            data = MsgPrcs.unpack_5f(buf)
            self.UAVinfo.update_u0(data)
        
        elif msgtype == MsgPrcs.PKGTYPE_U1:
            data = MsgPrcs.unpack_5f(buf)
            self.UAVinfo.update_u1(data)
            
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
            comm_options = pfio.load()
            self.sbar.update(u'默认通信设置"%s"已经应用。'%filepath)
        except (EOFError,IOError),e:
            self.m_statusBar.SetStatusText(u'未发现默认设置')
            comm_options = {}
        return comm_options
    
class InputHistory(object):
    '''
    输入区域历史记录管理器
    '''
    def __init__(self,window):
        '''
        初始化函数
        @param window:窗口
        '''
        self.window = window
        self.clear()
    
    def clear(self):
        '''
        清除记录
        '''
        self.history=[]
        self.cursor = -1
        
    def add(self,s):
        '''
        添加记录
        '''
        self.history.append(s)
        self.cursor = len(self.history)    
    
    def getByRel(self,rel):
        '''
        按相对位置获取记录
        @param rel: 相对位置
        @return: 记录内容，string
        '''
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
        '''
        按绝对位置获取记录
        @param cur: 绝对位置
        @return: 记录内容，string
        '''
        try:
            if cur == -1:
                raise IndexError
            ret = self.history[cur]
            self.window.SetStatusText("历史记录:%s"%ret,0)
        except IndexError:
            self.window.setStatusText("没有更多历史记录",0)
            ret = ""
        return ret