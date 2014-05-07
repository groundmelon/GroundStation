# -*- coding: utf-8 -*- 
'''
无人机信息存储

Created on 2014-3-13

@author: GroundMelon
'''
import util
import wx
import os
import time
from attitude.attitudeMod import AttitudeDisplay

LA = 45.732433
LO = 126.628802

INITVAL = float('NAN')

class InfoItem():
    '''
    一条信息代表的类
    '''
    def __init__(self, init_val=INITVAL):
        self.height = init_val
        self.pitch = init_val
        self.roll = init_val
        self.yaw = init_val
        self.volt = init_val
        self.posx = init_val
        self.posy = init_val
        self.rposx = init_val
        self.rposy = init_val
        self.sheight = init_val
        self.ref_thrust = init_val
        self.ref_pitch = init_val
        self.ref_yaw = init_val
        self.ref_roll = init_val
        self.ref_height = init_val
        self.PUp = init_val # Pitch Up
        self.PUi = init_val # Pitch Ui
        self.PUd = init_val # Pitch Ud
        self.RUp = init_val # Roll Up
        self.RUi = init_val
        self.RUd = init_val
        self.YUp = init_val
        self.YUi = init_val
        self.YUd = init_val
        self.st_ct = init_val # control type
        self.st_mt = init_val # motor state
        self.st_ah = init_val # auto height state
        self.st_sd = init_val # smart direction state
        self.uavtime = init_val
        self.la = LA
        self.lo = LO
    
    def add(self, name, value):
        '''
        向条目里添加元素
        @param name: 元素名
        @param value: 元素值
        '''
        if self.__dict__[name] is not INITVAL:
            # 将会覆盖已有信息
            raise self.OverrideError(name)
        else:
            self.__dict__[name] = value
    
    def __repr__(self):
        return str(self.__dict__)
        
    class OverrideError(Exception):
        def __init__(self, label):
            Exception.__init__(self, label)
            self.label = label
        def __repr__(self):
            return 'Override of %s'%self.label    

class UAVInfomation(object):
    '''
    无人机信息存储类
    '''
    def __init__(self):
        self.clear_buf()
        self.attidisp = AttitudeDisplay()
    
    def clear_buf(self):
        '''
        清楚信息存储缓冲区
        '''
        self.infobuf = [InfoItem()]
    
    def add_item(self):
        '''
        新增一个信息条目
        '''
        self.infobuf.append(InfoItem(INITVAL))
    
    def add_elements(self, keys, data):
        '''
        向当前条目里添加元素，按照key[0]-data[0],key[1]-data[1],...,key[4]-data[4]的顺序添加 
        @param keys: keys列表
        @param data: 数据列表
        '''
        while True:
            try:
                for index,key in enumerate(keys):
                    self.infobuf[-1].add(key, data[index])
                break;
            except (InfoItem.OverrideError,IndexError), e:
                # 若是有覆盖异常，说明需要在缓冲区里插入一个新的条目
                self.add_item()
        return
    
    def update_info(self, data):
        '''
        更新无人机姿态、高度、电压等信息
        '''
        self.add_elements(['roll','pitch','yaw','height','volt'], data)
    
    def update_pos(self, data):
        '''
        更新无人机位置、位置给定
        '''
        self.add_elements(['posx','posy','rposx','rposy','sheight'], data)
    
    def update_status(self, data):
        ''' 
        更新状态量
        @param data: 状态量数据
        @note: data is not data[0][1][2][3][4], cannot use add_elements '''
        while True:
            try:    
                self.infobuf[-1].add('st_ct', data[0])
                self.infobuf[-1].add('st_mt', data[1])
                self.infobuf[-1].add('st_ah', data[2])
                self.infobuf[-1].add('st_sd', data[3])
                self.infobuf[-1].add('uavtime', data[-1])
                break
            except InfoItem.OverrideError:
                self.add_item()
            except IndexError:
                self.add_item()
        return
    
    def update_ref(self, data):
        '''
        更新给定信息
        '''
        self.add_elements(['ref_roll','ref_pitch','ref_yaw','ref_thrust','ref_height'], data)
        self.infobuf[-1].height = self.infobuf[-1].height/100.0
    
    def update_u0(self, data):
        '''
        更新控制量信息之0
        '''
        self.add_elements(['RUp','RUi','RUd','PUp','PUi'], data)
         
    def update_u1(self, data):
        '''
        更新控制量信息之1
        '''
        self.add_elements(['PUd','YUp','YUi','YUd'], data)
        
    def get_by_index(self, index):
        '''
        按索引获得信息条目
        @param index: 索引号
        @return: 第index个条目
        '''
        try:
            data = self.infobuf[index]
        except IndexError:
            data = self.infobuf[-1]
        return data

    def get(self, index=-1):
        '''
        默认获得最后一个信息条目
        @param index: 索引号
        @return: 第index个条目，默认最后一个
        '''
        return self.get_by_index(index)
    
    def get_attitude_img(self, pitch, roll, yaw):
        '''
        按索引获得信息条目
        @param index: 索引号
        @return: 第index个条目
        '''
        return self.attidisp.generate_attitude_bitmap(pitch, 
                                                      roll, 
                                                      yaw, 
                                                      is_radius= False)
    
    def need_warning(self, key, value):
        '''
        判断某个信息是否需要报警
        @param key: 信息key
        @param value: 信息value
        @return: 需要警报True，不需警报False 
        '''
        if 'height' == key and value < 1:
            return True
        elif 'volt' == key and value < 11.3:
            return True
        else:
            return False
            
    
    def get_information_in_InfoEntries(self):
        '''
        用L{InfoEntry<GroundStation.util.InfoEntry>}的方式输出信息条目
        @return: a list of InfoEntries
        '''
        rtnval = []
        info = self.get()
        entry_type = util.InfoEntry.TYPE_WARNING if self.need_warning('height', info.height) else util.InfoEntry.TYPE_LABEL        
        rtnval.append(util.InfoEntry(entry_type,'Height', ''.join(['%4.4f'%info.height,'m'])))
        
        entry_type = util.InfoEntry.TYPE_LABEL       
        rtnval.append(util.InfoEntry(entry_type,'Pitch', ''.join(['%4.4f'%(info.pitch),'d'])))
        
        entry_type = util.InfoEntry.TYPE_LABEL       
        rtnval.append(util.InfoEntry(entry_type,'Roll', ''.join(['%4.4f'%(info.roll),'d'])))
        
        entry_type = util.InfoEntry.TYPE_LABEL        
        rtnval.append(util.InfoEntry(entry_type,'Yaw', ''.join(['%4.4f'%(info.yaw),'d'])))
        
        entry_type = util.InfoEntry.TYPE_WARNING if self.need_warning('volt', info.volt) else util.InfoEntry.TYPE_LABEL        
        rtnval.append(util.InfoEntry(entry_type,'Volt', ''.join(['%4.4f'%(info.volt),'v'])))
        
        entry_type = util.InfoEntry.TYPE_LABEL
        rtnval.append(util.InfoEntry(entry_type,'Pos', ''.join(['(%5.2f,%5.2f)'%(info.posx,info.posy)])))
        
        return rtnval
    
    def save_to_file(self, window, pidpara = None):
        '''
        把无人机信息输出到文件中。弹出一个FilePicker窗口选择文件
        @param window: window对象，用于状态栏更新的
        @param pidpara: 默认None，若传入list则打印PID参数信息于文件头 
        '''
        filename=u'Rec '+time.strftime('%m-%d %H.%M')
        dialog = wx.FileDialog(None, u"保存UAV信息到...", '',filename, u"文本文件 (*.txt)|*.txt", wx.SAVE)
        if dialog.ShowModal() == wx.ID_OK:
            filepath = dialog.GetPath()
        else:
            filepath = None
        dialog.Destroy()
        
        if filepath: # Filepicker Dialoag OK
            with open(filepath,'w') as f:
                if pidpara:# 需要打印PID参数信息
                    assert len(pidpara) == 20, 'pidpara length error'
                    # print titles
                    f.write('XP\tXI\tXD\tXSP\tYP\tYI\tYD\tYSP\tZP\tZI\tZD\tZSP\tHP\tHI\tHD\tHSP\tPP\tPI\tPD\tPSP\n')
                    # print numbers
                    f.write('%s\n'%('\t'.join(['%f'%x for x in pidpara])))
                    
                items = ['height','pitch','roll','yaw','volt','Rpitch','Rroll','Ryaw',
                         'Rthr','Rheight','posx','posy','Rposx','Rposy','Sheight','la','lo','PUp',
                         'PUi','PUd','RUp','RUi','RUd','YUp','YUi','YUd','UAVTIME']
                # print titles
                s='No.%s\n'%('\t'.join([ '%d%s'%(index+1,item) for index,item in enumerate(items)]))
                f.write(s)
                
                for i in range(len(self.infobuf)):
                    # print numbers
                    data = self.infobuf[i]
                    lst = []
                    lst.append('%s\t'%str(data.height))
                    lst.append('%s\t'%str(data.pitch))
                    lst.append('%s\t'%str(data.roll))
                    lst.append('%s\t'%str(data.yaw))
                    lst.append('%s\t'%str(data.volt))
                    lst.append('%s\t'%str(data.ref_pitch))
                    lst.append('%s\t'%str(data.ref_roll))
                    lst.append('%s\t'%str(data.ref_yaw))
                    lst.append('%s\t'%str(data.ref_thrust))
                    lst.append('%s\t'%str(data.ref_height))
                    lst.append('%s\t'%str(data.posx))
                    lst.append('%s\t'%str(data.posy))
                    lst.append('%s\t'%str(data.rposx))
                    lst.append('%s\t'%str(data.rposy))
                    lst.append('%s\t'%str(data.sheight))
                    lst.append('%s\t'%str(data.la))
                    lst.append('%s\t'%str(data.lo))
                    lst.append('%s\t'%str(data.PUp))
                    lst.append('%s\t'%str(data.PUi))
                    lst.append('%s\t'%str(data.PUd))
                    lst.append('%s\t'%str(data.RUp))
                    lst.append('%s\t'%str(data.RUi))
                    lst.append('%s\t'%str(data.RUd))
                    lst.append('%s\t'%str(data.YUp))
                    lst.append('%s\t'%str(data.YUi))
                    lst.append('%s\t'%str(data.YUd))
                    lst.append('%s\t'%str(data.uavtime))
                    lst.append('\n')
                    f.write(''.join(lst))
                
                # close file
                f.close()
            window.sbar.update(u'UAV信息已经保存。')
            return True #saved
        else:# Filepicker Dialoag Cancelled
            return False
    