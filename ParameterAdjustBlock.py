# -*- coding: utf-8 -*- 
'''
Created on 2014-3-18

@author: GroundMelon
'''
from GroundStationBase import FrameGroundStationBase
import communication.MessageProcess as MsgPrcs
import os

PARA_LOOK_DIV_REAL=1000.0
PARA_FILE_PATH = os.getcwd() + r'\resources\para.dat'

class ParameterAdjustBlock():
    def init_para_block(self):
        para = self.read_para_from_file()
        self.write_para_to_table(para)
        self.rcv_pid = {'XP':float('nan'), 'XI':float('nan'), 'XD':float('nan'), 'XSP':float('nan'),
                        'YP':float('nan'), 'YI':float('nan'), 'YD':float('nan'), 'YSP':float('nan'),
                        'ZP':float('nan'), 'ZI':float('nan'), 'ZD':float('nan'), 'ZSP':float('nan'),
                        'HP':float('nan'), 'HI':float('nan'), 'HD':float('nan'), 'HSP':float('nan'),
                        'PP':float('nan'), 'PI':float('nan'), 'PD':float('nan'), 'PSP':float('nan'),
                        }
    
    def write_para_to_table(self, para):
        assert len(para) == self.m_grid_para_adj.GetNumberRows(), 'indices of para error.'
        for index in range(self.m_grid_para_adj.GetNumberRows()):
            assert isinstance(para[index], float)
            self.m_grid_para_adj.SetCellValue(index,0,str(para[index]*PARA_LOOK_DIV_REAL))
    
    def get_para_from_table(self):
        para = []
        for index in range(self.m_grid_para_adj.GetNumberRows()):
            para.append(float(self.m_grid_para_adj.GetCellValue(index,0))/PARA_LOOK_DIV_REAL)
        return para
    
    def save_para(self):
        with open(PARA_FILE_PATH,'w') as f:
            for data in self.get_para_from_table():
                f.write('%s\n'%str(data))
        self.sbar.update(u'参数已成功保存')
    
    def read_para_from_file(self):
        para = []
        with open(PARA_FILE_PATH,'r') as f:
            for line in f.readlines():
                para.append(float(line))
        return para
    
    def load_para(self):
        para = self.read_para_from_file()
        self.write_para_to_table(para)
        self.sbar.update(u'参数已成功读取')
    
    def send_para(self, msk = (True, True, True, True, True)):
        para = self.get_para_from_table()
        rtn = 0
        if msk[0]:
            rtn = self.send_data_by_frame(MsgPrcs.pack_adj_pid_para(para[:4], 'X'))
        if msk[1]:
            rtn = self.send_data_by_frame(MsgPrcs.pack_adj_pid_para(para[4:8], 'Y'))
        if msk[2]:
            rtn = self.send_data_by_frame(MsgPrcs.pack_adj_pid_para(para[8:12], 'Z'))
        if msk[3]:    
            rtn = self.send_data_by_frame(MsgPrcs.pack_adj_pid_para(para[12:16], 'H'))
        if msk[4]:
            rtn = self.send_data_by_frame(MsgPrcs.pack_adj_pid_para(para[16:20], 'P'))
        
        self.sbar.update(u'参数已经发送(%d)'%rtn)
    
    def set_down_para(self):
        data = MsgPrcs.pack_set_pid_para()
        rtn = self.send_data_by_frame(data)
        self.sbar.update(u'参数已经固定(%d)'%rtn)
    
    def update_rcv_pid(self, axis, para):
        if axis in ['X','Y','Z','H','P']:
            self.rcv_pid['%sP'%axis] = para[0]
            self.rcv_pid['%sI'%axis] = para[1]
            self.rcv_pid['%sD'%axis] = para[2]
            self.rcv_pid['%sSP'%axis] = para[3]
        self.show_rcv_pid()
        
    def show_rcv_pid(self):
        title = u'机上PID参数\n\n'
        info = ''.join(['%s = %6.2f/K\n'%(t.rjust(3,' '), self.rcv_pid[t]*PARA_LOOK_DIV_REAL)
                        for t in ['XP','XI','XD','XSP',
                                  'YP','YI','YD','YSP',
                                  'ZP','ZI','ZD','ZSP',
                                  'HP','HI','HD','HSP',
                                  'PP','PI','PD','PSP',
                                  ]
                        ])
        self.m_staticText_showpid.SetLabel(''.join([title, info]))
        