# -*- coding: utf-8 -*- 
'''
Created on 2014-3-13

@author: GroundMelon
'''
import util
import wx
import os
from attitude.attitudeMod import AttitudeDisplay

LA = 45.732433
LO = 126.628802

class InfoItem():
    def __init__(self, init_val=None):
        self.height = init_val
        self.pitch = init_val
        self.roll = init_val
        self.yaw = init_val
        self.volt = init_val
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
        if self.__dict__[name] is not None:
            raise self.OverrideException(name)
        else:
            self.__dict__[name] = value
    
    def __repr__(self):
        return str(self.__dict__)
        
    class OverrideException(Exception):
        def __init__(self, label):
            Exception.__init__(self, label)
            self.label = label
        def __repr__(self):
            return 'Override of %s'%self.label    

class UAVInfomation(object):
    def __init__(self):
        self.clear_buf()
        self.attidisp = AttitudeDisplay()
    
    def clear_buf(self):
        self.infobuf = [InfoItem()]
    
    def add_item(self):
        self.infobuf.append(InfoItem(None))
    
    def update_info(self, roll, pitch, yaw, height, volt):
        while True:
            try:
                self.infobuf[-1].add('roll', roll)
                self.infobuf[-1].add('pitch', pitch)
                self.infobuf[-1].add('yaw', yaw)
                self.infobuf[-1].add('height', height/100.0)
                self.infobuf[-1].add('volt', volt)
                break
            except InfoItem.OverrideException, e:
                self.add_item()
            except IndexError, e:
                self.add_item()
        return
    
    def update_status(self, data):
        while True:
            try:    
                self.infobuf[-1].add('st_ct', data[0])
                self.infobuf[-1].add('st_mt', data[1])
                self.infobuf[-1].add('st_ah', data[2])
                self.infobuf[-1].add('st_sd', data[3])
                self.infobuf[-1].add('uavtime', data[-1])
                break
            except InfoItem.OverrideException:
                self.add_item()
            except IndexError:
                self.add_item()
        return
    
    def update_ref(self, ref_roll, ref_pitch, ref_yaw, ref_thrust, ref_height):
        while True:
            try:
                self.infobuf[-1].add('ref_roll', ref_roll)
                self.infobuf[-1].add('ref_pitch', ref_pitch)
                self.infobuf[-1].add('ref_yaw', ref_yaw)
                self.infobuf[-1].add('ref_thrust', ref_thrust)
                self.infobuf[-1].add('ref_height', ref_height/100.0)
                break
            except InfoItem.OverrideException, e:
                self.add_item()
            except IndexError, e:
                self.add_item()
        return
        
    
    def update_u0(self, RUp, RUi, RUd, PUp, PUi,):
        while True:
            try:
                self.infobuf[-1].add('RUp', RUp)
                self.infobuf[-1].add('RUi', RUi)
                self.infobuf[-1].add('RUd', RUd)
                self.infobuf[-1].add('PUp', PUp)
                self.infobuf[-1].add('PUi', PUi)
                break
            except InfoItem.OverrideException, e:
                self.add_item()
            except IndexError, e:
                self.add_item()
        return
         
    def update_u1(self, PUd, a, b, c, uavtime):
        while True:
            try:
                self.infobuf[-1].add('PUd', PUd)
                self.infobuf[-1].add('YUp', a)
                self.infobuf[-1].add('YUi', b)
                self.infobuf[-1].add('YUd', c)
#                 self.infobuf[-1].add('st_mt', a)
#                 self.infobuf[-1].add('st_ah', b)
#                 self.infobuf[-1].add('st_sd', c)
#                 self.infobuf[-1].add('uavtime', uavtime)
                break
            except InfoItem.OverrideException, e:
                self.add_item()
            except IndexError, e:
                self.add_item()
        return
        
    def get_by_index(self, index):
        data = self.infobuf[index]
        return {'height': data.height,
                'pitch': data.pitch,
                'roll': data.roll,
                'yaw': data.yaw,
                'volt': data.volt,
                'la': data.la,
                'lo': data.lo,
                'ref_pitch': data.ref_pitch,
                'ref_roll': data.ref_roll,
                'ref_yaw': data.ref_yaw,
                'ref_thrust': data.ref_thrust,
                'ref_height': data.ref_height,
                'uavtime': data.uavtime,
                'st_mt': data.st_mt,
                'st_ah': data.st_ah,
                'st_sd': data.st_sd,
                'st_ct': data.st_ct
                }
    def get(self, index=-1):
        return self.get_by_index(index)
    
    def get_attitude_img(self):
        info = self.get()
        return self.attidisp.generate_attitude_bitmap(info['pitch'], 
                                                      info['roll'], 
                                                      info['yaw'], 
                                                      is_radius= False)
    
    def need_warning(self, key, value):
        if 'height' == key and value < 1:
            return True
        elif 'volt' == key and value < 11.3:
            return True
        else:
            return False
            
    
    def get_information_in_InfoEntries(self):
        rtnval = []
        info = self.get()
        
        entry_type = util.InfoEntry.TYPE_WARNING if self.need_warning('height', info['height']) else util.InfoEntry.TYPE_LABEL        
        rtnval.append(util.InfoEntry(entry_type,'Height', ''.join([str(info['height']),'m'])))
        
        entry_type = util.InfoEntry.TYPE_LABEL       
        rtnval.append(util.InfoEntry(entry_type,'Pitch', ''.join([str(info['pitch']),'d'])))
        
        entry_type = util.InfoEntry.TYPE_LABEL       
        rtnval.append(util.InfoEntry(entry_type,'Roll', ''.join([str(info['roll']),'d'])))
        
        entry_type = util.InfoEntry.TYPE_LABEL        
        rtnval.append(util.InfoEntry(entry_type,'Yaw', ''.join([str(info['yaw']),'d'])))
        
        entry_type = util.InfoEntry.TYPE_WARNING if self.need_warning('volt', info['volt']) else util.InfoEntry.TYPE_LABEL        
        rtnval.append(util.InfoEntry(entry_type,'Volt', ''.join([str(info['volt']),'v'])))
        
        return rtnval
    
    def save_to_file(self, window, pidpara = None):
        dialog = wx.FileDialog(None, u"保存UAV信息到...", '',u"", u"文本文件 (*.txt)|*.txt", wx.SAVE)
        if dialog.ShowModal() == wx.ID_OK:
            filepath = dialog.GetPath()
        else:
            filepath = None
        dialog.Destroy()
        if filepath:
            try:
                with open(filepath,'w') as f:
                    if pidpara:
                        assert len(pidpara) == 16, 'pidpara length error'
                        f.write('XP\tXI\tXD\tXSP\tYP\tYI\tYD\tYSP\tZP\tZI\tZD\tZSP\tHP\tHI\tHD\tHSP\n')
                        f.write('%s\n'%('\t'.join(['%f'%x for x in pidpara])))
                    f.write('No.1height\t2pitch\t3roll\t4yaw\t5volt\t6Rpitch\t7Rroll\t8Ryaw\t9Rthr\t10Rheight\t11la\t12lo')
                    f.write('\t13PUp\t14PUi\t15PUd\t16RUp\t17RUi\t18RUd\t19YUp\t20YUi\t21YUd\t22UAVTime\n')
                    for i in range(len(self.infobuf)):
                        lst = []
                        data = self.infobuf[i]
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
                        f.write((''.join(lst)).replace('None', '0.0'))
                    f.close()
                window.sbar.update(u'UAV信息已经保存。')
            except Exception,e:
                wx.MessageBox(u'UAV信息保存失败。\n%s'%(str(e)), u"保存失败",wx.OK | wx.ICON_ERROR)
                window.sbar.update(u'UAV信息保存发生错误')    
    
    def _test_save_to_file(self, filepath='test.txt', pidpara=None):
        with open(filepath,'w') as f:
            if pidpara:
                assert len(pidpara) == 16, 'pidpara length error'
                f.write('XP\tXI\tXD\tXSP\tYP\tYI\tYD\tYSP\tZP\tZI\tZD\tZSP\tHP\tHI\tHD\tHSP\n')
                f.write('%s\n'%('\t'.join(['%f'%x for x in pidpara])))
            f.write('No.1height\t2pitch\t3roll\t4yaw\t5volt\t6Rpitch\t7Rroll\t8Ryaw\t9Rthr\t10Rheight\t11la\t12lo')
            f.write('\t13PUp\t14PUi\t15PUd\t16RUp\t17RUi\t18RUd\t19YUp\t20YUi\t21YUd\t22UAVTime\n')
            for i in range(len(self.infobuf)):
                data = self.infobuf[i]
                lst = []
                data = self.infobuf[i]
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
            f.close()

if __name__ == '__main__':
    x=UAVInfomation()
    x.update_info(1, 2, 3, 4, 5)
    x.update_info(2, 3, 4, 5, 6)
    x._test_save_to_file()