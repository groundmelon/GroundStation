# -*- coding: utf-8 -*- 
'''
Created on 2014-4-1

@author: GroundMelon
'''

from GroundStationBase import VideoSettingDialog
from imageprocess.ImageCapture import get_dev_num_list


class VideoSetting(VideoSettingDialog):
    def __init__(self, parent, sel=0):
        VideoSettingDialog.__init__(self, parent)
        devs = get_dev_num_list()
        self.m_choice.SetItems([str(x) for x in devs])
        if sel in devs:
            self.m_choice.SetSelection(sel)
        else:
            self.m_choice.SetSelection(0)
    
    def get_dev_num(self):
        return self.m_choice.GetSelection()