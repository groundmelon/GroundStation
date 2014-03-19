# -*- coding: utf-8 -*- 
'''
Created on 2014-3-18

@author: GroundMelon
'''
from GroundStationBase import FrameGroundStationBase
import struct

PARA_FILE_PATH = r'para.dat'

class ParameterAdjustBlock():
    def init_para_adj_table(self):
        para = [1.0, 1.0, 1.0,
                1.0, 1.0, 1.0,
                1.0, 1.0, 1.0]
        self.write_para_to_table(para)
    
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
    
    def load_para(self):
        para = []
        with open(PARA_FILE_PATH,'r') as f:
            for line in f.readlines():
                para.append(float(line))
        self.write_para_to_table(para)
    
    def send_para(self):
        para = self.get_para_from_table()
        head = struct.pack('2B', 0xAA, 0x55)
        end = struct.pack('2B', 0xDD, 0xEE)
        body = ''.join([struct.pack('f',val) for val in para])
        data = ''.join([head, body, end])
        self.send_data_by_frame(data)
    
    def set_down_para(self):
        head = struct.pack('2B', 0xAA, 0x66)
        end = struct.pack('2B', 0xDD, 0xEE)
        body = '\x00'*4*9
        data = ''.join([head, body, end])
        self.send_data_by_frame(data)
        