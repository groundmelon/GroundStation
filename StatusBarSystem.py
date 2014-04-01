# -*- coding: utf-8 -*- 
'''
Created on 2014-3-19

@author: GroundMelon
'''

class StatusBarSystem():
    def __init__(self, sb):
        self.sb = sb;
        self.his=([''],[''])

    def update(self, content, index = 0):
        assert isinstance(content, unicode) or isinstance(content, str)
        self.sb.SetStatusText(content, index)
        self.his[index].append(content)
        if len(self.his[index])>100:
            self.his[index].pop(0)
    
    def backward(self, index = 0):
        self.his[index].pop()
        self.sb.SetStatusText(self.his[index][-1], index)