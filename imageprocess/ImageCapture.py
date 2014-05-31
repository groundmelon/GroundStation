# -*- coding: utf-8 -*- 
'''
Created on 2014-4-1

@author: GroundMelon
'''

from VideoCapture import Device
from VideoCapture import vidcap
import numpy as np

def get_dev_num_list():
    '''
    获得视频设备的数目
    @return: 返回一个表示设备数目的列表
    '''
    dev = []
    for i in range(5):
        try:
            cam = Device(i)
            dev.append(i)
        except vidcap.error:
            pass
    return dev


class ImageCapture():
    '''
    图像采集类
    '''
    NoDeviceError = vidcap.error
    def __init__(self, devnum=0):
        '''
        初始化
        @param devnum: 设备号
        '''
        self.cam = Device(devnum)
        # TODO: 卡死保护
#         self.cam.displayCaptureFilterProperties()
#         self.cam.displayCapturePinProperties()
        cvimg = np.array(self.cam.getImage().convert('RGB'))
        self.size = (cvimg.shape[1],cvimg.shape[0])
    
    def get_frame_size(self):
        '''
        获取帧大小
        @return: 帧的大小 
        '''
        return self.size
    
    def get_frame(self):
        '''
        获取当前帧
        @return: 当前帧
        '''    
        im_pil = self.cam.getImage().convert('RGB')
        cvimg = np.array(im_pil)
        return cvimg[:,:,::-1] # opencv的默认图像制式是 BGR
    
    def release(self):
        '''
        释放摄像头
        '''
        print 'Release Camera'
        del self.cam


if __name__ == '__main__':
    cam = ImageCapture(1)
    print get_dev_num_list()