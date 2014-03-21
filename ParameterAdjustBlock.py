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
        para = [1.0, 1.0, 1.0,
                1.0, 1.0, 1.0,
                1.0, 1.0, 1.0]
        self.write_para_to_table(para)
        self.rcv_pid = {'XP':1.0, 'XI':1.0, 'XD':1.0,
                        'YP':1.0, 'YI':1.0, 'YD':1.0,
                        'ZP':1.0, 'ZI':1.0, 'ZD':1.0,}
    
    def write_para_to_table(self, para):
        assert len(para) == self.m_grid_para_adj.GetNumberRows(), 'indices of para error.'
        for index in range(self.m_grid_para_adj.GetNumberRows()):
            assert isinstance(para[index], float)
            self.m_grid_para_adj.SetCellValue(index,0,str(para[index]))
    
    def get_para_from_table(self):
        para = []
        for index in range(self.m_grid_para_adj.GetNumberRows()):
            para.append(float(self.m_grid_para_adj.GetCellValue(index,0)))
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
    
    def send_para(self):
        para = self.get_para_from_table()
        
        self.send_data_by_frame(MsgPrcs.pack_adj_pid_para(para[:3], 'X'))
        self.send_data_by_frame(MsgPrcs.pack_adj_pid_para(para[3:6], 'Y'))
        self.send_data_by_frame(MsgPrcs.pack_adj_pid_para(para[6:], 'Z'))
        
        self.sbar.update(u'参数已经发送')
    
    def set_down_para(self):
        data = MsgPrcs.pack_set_pid_para()
        self.send_data_by_frame(data)
        self.sbar.update(u'参数已经固定')
    
    def update_rcv_pid(self, axis, para):
        self.rcv_pid['%sP'%axis] = para[0]
        self.rcv_pid['%sI'%axis] = para[1]
        self.rcv_pid['%sD'%axis] = para[2]
        self.show_rcv_pid()
        
    def show_rcv_pid(self):
        title = u'机上PID参数\n\n'
        info = ''.join(['%s = %.4f\n'%(t, self.rcv_pid[t])
                        for t in ['XP','XI','XD','YP','YI','YD','ZP','ZI','ZD']
                        ])
        self.m_textCtrl_showpid.SetValue(''.join([title, info]))
        