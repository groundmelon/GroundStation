# -*- coding: utf-8 -*- 
'''
Created on 2014-3-13

@author: GroundMelon
'''
import util
from attitude.attitudeMod import AttitudeDisplay
from traitsui.view import Height

class UAVInfomation(object):
    def __init__(self):
        self.height = [0]
        self.pitch = [0]
        self.roll = [0]
        self.yaw = [0]
        self.vol = [0]
        self.la = [45.732433]
        self.lo = [126.628802]
        self.attidisp = AttitudeDisplay()
    
    def update(self, roll, pitch, yaw, height, vol, la, lo):
        if height:
            self.height.append(height/100)
        else:
            self.height.append(self.get()['height'])
        
        if pitch:
            self.pitch.append(pitch)
        else:
            self.pitch.append(self.get()['pitch'])
        
        if roll:
            self.roll.append(roll)
        else:
            self.roll.append(self.get()['roll'])
        
        if yaw:
            self.yaw.append(yaw)
        else:
            self.yaw.append(self.get()['yaw'])
        
        if vol:
            self.vol.append(vol)
        else:
            self.vol.append(self.get()['vol'])
        
        if la:
            self.la.append(la)
        else:
            self.la.append(self.get()['la'])
        
        if lo:
            self.lo.append(lo)
        else:
            self.lo.append(self.get()['lo'])
        
    def get_by_index(self, index):
        return {'height': self.height[index],
                'pitch': self.pitch[index],
                'roll': self.roll[index],
                'yaw': self.yaw[index],
                'vol': self.vol[index],
                'la': self.la[index],
                'lo': self.lo[index],
                }
    def get(self):
        return self.get_by_index(-1)
    
    def get_attitude_img(self):
        info = self.get()
        return self.attidisp.generate_attitude_bitmap(info['pitch'], 
                                                      info['roll'], 
                                                      info['yaw'], 
                                                      is_radius= False)
    
    def need_warning(self, key, value):
        if 'height' == key and value < 1:
            return True
        elif 'vol' == key and value < 11.3:
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
        
        entry_type = util.InfoEntry.TYPE_WARNING if self.need_warning('vol', info['vol']) else util.InfoEntry.TYPE_LABEL        
        rtnval.append(util.InfoEntry(entry_type,'Voltage', ''.join([str(info['vol']),'v'])))
        
        return rtnval