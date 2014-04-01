# -*- coding: utf-8 -*- 
'''
Created on 2014-4-1

@author: GroundMelon
'''

from GroundStationBase import VideoSettingDialog
from imageprocess.ImageCapture import DEV_NUM_LIST


class VideoSetting(VideoSettingDialog):
    def __init__(self, parent):
        VideoSettingDialog.__init__(self, parent)
        self.m_choice.SetItems([str(x) for x in DEV_NUM_LIST])
    
    def get_dev_num(self):
        self.m_choice.GetSelection()