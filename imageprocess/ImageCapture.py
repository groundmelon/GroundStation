# -*- coding: utf-8 -*- 
'''
Created on 2014-4-1

@author: GroundMelon
'''

from VideoCapture import Device
from VideoCapture import vidcap
import numpy as np

def get_dev_num_list():
    dev = []
    for i in range(5):
        try:
            cam = Device(i)
            dev.append(i)
        except vidcap.error:
            pass
    return dev

DEV_NUM_LIST = get_dev_num_list()


class ImageCapture():
    NoDeviceError = vidcap.error
    def __init__(self, devnum):
        self.cam = Device(devnum)
#         self.cam.displayCaptureFilterProperties()
#         self.cam.displayCapturePinProperties()
        cvimg = np.array(self.cam.getImage().convert('RGB'))
        
        self.size = (cvimg.shape[1],cvimg.shape[0])
    
    def get_frame_size(self):
        return self.size
    
    def get_frame(self):    
        im_pil = self.cam.getImage().convert('RGB')
        cvimg = np.array(im_pil)
        return cvimg[:,:,::-1]
    
    def release(self):
        print 'done release'
        del self.cam

if __name__ == '__main__':
    print get_dev_num_list()