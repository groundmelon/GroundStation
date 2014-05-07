# -*- coding: utf-8 -*- 
'''
Created on 2014-2-12

@author: GroundMelon
'''
from GroundStationBase import FrameGroundStationBase
from Definition import *

class WorkBlock(FrameGroundStationBase, object):
    def init_worklist(self):
        #self.worklist = [DISPLAY_ATTITUDE]
        self.worklist = []
    def add_work(self, work):
        if work not in self.worklist:
            self.worklist.append(work)
        else:
            
            assert False, 'Work%s is already in work list!' \
                            %str([k for k,v in DEFINITION_LOCALS_DICT.iteritems() if v == work])
    
    def remove_work(self, work):
        if work in self.worklist:
            self.worklist.remove(work)
        else:
            assert False, 'Cannot find work%s in work list!' \
                            %str([k for k,v in DEFINITION_LOCALS_DICT.iteritems() if v == work])
    
    def find_work(self, work):
        if work in self.worklist:
            return True
        else:
            return False
            
        