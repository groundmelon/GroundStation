# -*- coding: utf-8 -*- 
'''
Created on 2014-3-18

@author: GroundMelon
'''
from GroundStationBase import FrameGroundStationBase
import communication.MessageProcess as MsgPrcs

PARA_FILE_PATH = r'para.dat'

class ParameterAdjustBlock():
    def init_para_block(self):
        para = [0.0, 0.0, 0.0, 0.0, 
                0.0, 0.0, 0.0, 0.0, 
                0.0, 0.0, 0.0, 0.0,
                0.0, 0.0, 0.0, 0.0]
        self.write_para_to_table(para)
        self.rcv_pid = {'XP':0.0, 'XI':0.0, 'XD':0.0, 'XSP':0.0,
                        'YP':0.0, 'YI':0.0, 'YD':0.0, 'YSP':0.0,
                        'ZP':0.0, 'ZI':0.0, 'ZD':0.0, 'ZSP':0.0,
                        'HP':0.0, 'HI':0.0, 'HD':0.0, 'HSP':0.0,
                        }
    
    def write_para_to_table(self, para):
        assert len(para) == self.m_grid_para_adj.GetNumberRows(), 'indices of para error.'
        for index in range(self.m_grid_para_adj.GetNumberRows()):
            assert isinstance(para[index], float)
            self.m_grid_para_adj.SetCellValue(index,0,str(para[index]*1000))
    
    def get_para_from_table(self):
        para = []
        for index in range(self.m_grid_para_adj.GetNumberRows()):
            para.append(float(self.m_grid_para_adj.GetCellValue(index,0))/1000.0)
        return para
    
    def save_para(self):
        with open(PARA_FILE_PATH,'w') as f:
            for data in self.get_para_from_table():
                f.write('%s\n'%str(data))
        self.sbar.update(u'参数已成功保存')
    
    def load_para(self):
        para = []
        with open(PARA_FILE_PATH,'r') as f:
            for line in f.readlines():
                para.append(float(line))
        self.write_para_to_table(para)
        self.sbar.update(u'参数已成功读取')
    
    def send_para(self, msk = (True, True, True, True)):
        para = self.get_para_from_table()
        rtn = 0
        if msk[0]:
            rtn = self.send_data_by_frame(MsgPrcs.pack_adj_pid_para(para[:4], 'X'))
        if msk[1]:
            rtn = self.send_data_by_frame(MsgPrcs.pack_adj_pid_para(para[4:8], 'Y'))
        if msk[2]:
            rtn = self.send_data_by_frame(MsgPrcs.pack_adj_pid_para(para[8:12], 'Z'))
        if msk[3]:    
            rtn = self.send_data_by_frame(MsgPrcs.pack_adj_pid_para(para[12:], 'H'))
        
        self.sbar.update(u'参数已经发送(%d)'%rtn)
    
    def set_down_para(self):
        data = MsgPrcs.pack_set_pid_para()
        rtn = self.send_data_by_frame(data)
        self.sbar.update(u'参数已经固定(%d)'%rtn)
    
    def update_rcv_pid(self, axis, para):
        if axis in ['X','Y','Z','H']:
            self.rcv_pid['%sP'%axis] = para[0]
            self.rcv_pid['%sI'%axis] = para[1]
            self.rcv_pid['%sD'%axis] = para[2]
            self.rcv_pid['%sSP'%axis] = para[3]
        self.show_rcv_pid()
        
    def show_rcv_pid(self):
        title = u'机上PID参数\n\n'
        info = ''.join(['%s=%s/K\n'%(t.ljust(3,' '), ('%.3f'%(self.rcv_pid[t]*1000)).rjust(7,' '))
                        for t in ['XP','XI','XD','XSP',
                                  'YP','YI','YD','YSP',
                                  'ZP','ZI','ZD','ZSP',
                                  'HP','HI','HD','HSP']
                        ])
        self.m_textCtrl_showpid.SetValue(''.join([title, info]))
        