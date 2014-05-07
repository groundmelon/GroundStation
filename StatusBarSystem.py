# -*- coding: utf-8 -*- 
'''
Created on 2014-3-19

@author: GroundMelon
'''

class StatusBarSystem():
    '''
            状态栏管理系统
    '''
    def __init__(self, sb):
        '''
        @param sb:状态栏实例
        '''
        self.sb = sb;
        self.his=([''],[''])#：状态栏历史,有个状态栏block，故有两个列表

    def update(self, content, index = 0):
        '''
        更新状态栏
        @param content:更新的内容，unicode or string
        @param index:取值0或1，更新的位置，状态栏0区还是1区
        '''
        assert isinstance(content, unicode) or isinstance(content, str)
        assert index==0 or index==1
        self.sb.SetStatusText(content, index)
        self.his[index].append(content)
        # 限制历史记录长度
        if len(self.his[index])>100:
            self.his[index].pop(0)
    
    def backward(self, index = 0):
        '''
        回退状态栏，使状态栏显示上一步的信息
        @param index:取值0或1，更新的位置，状态栏0区还是1区
        '''
        self.his[index].pop()
        self.sb.SetStatusText(self.his[index][-1], index)