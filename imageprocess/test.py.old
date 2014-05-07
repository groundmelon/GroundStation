# -*- coding: utf-8 -*- 
'''
Created on 2013-12-27

@author: GroundMelon

@note: 测试一些图像处理方法，在确定之后会整理，形成结构化的代码

'''
import cv2
import numpy as np
from multiprocessing import *

DRAG_COLOR = (255,0,0)
OBJECT_MATCH_COLOR = (0, 0, 255)

class StaticTest(object):
    ''' 静态图片识别测试类 '''
    def __init__(self, frame_bitmap_size):
        self.image_adjust_settings = {'Brightness':50,
                                      'Contrast':50,
                                      'Gamma':50,
                                      }
        # 主窗口中bitmap的可视尺寸
        self.frame_bitmap_size = tuple(frame_bitmap_size)
        
        img_name = ['0.jpg','1.jpg','2.jpg','2r.jpg']
        self.img = []
        for name in img_name:
            self.img.append(cv2.imread(r'F:\Workplace\GroundStation\imageprocess\shuihu\%s'%name,cv2.IMREAD_COLOR))
        
        #img = cv2.resize(img, (320, 240), interpolation = cv2.INTER_CUBIC)
        self.srcimg = self.img[0]
        self.img_index = 0
       
    def next(self):
        self.img_index = (self.img_index+1) % 4
        self.srcimg = self.img[self.img_index]
    
    def cvimg_to_imgdata(self,cvimg):
        
        imgsrc = cv2.cvtColor(np.uint8(cvimg), cv2.COLOR_BGR2RGB)
        imgrsz = cv2.cvtColor(np.uint8(cv2.resize(cvimg, self.frame_bitmap_size, interpolation = cv2.INTER_CUBIC)),
                              cv2.COLOR_BGR2RGB)
        
        return {'src':(imgsrc.shape[1], imgsrc.shape[0], imgsrc),
                'rsz':(imgrsz.shape[1], imgrsz.shape[0], imgrsz),
                }
    
    def get_source(self):                
        return self.cvimg_to_imgdata(self.srcimg)
    
    def adjust_by_settings(self, src):
        dst = ((src * (self.image_adjust_settings['Brightness']/50.0) 
               + (self.image_adjust_settings['Contrast']-50)*2
               )**(self.image_adjust_settings['Gamma']/50.0))                   
        
        # 把大于255的部分设置为255
        dst_255_mask = np.greater_equal(dst,255)
        dst[dst_255_mask] = 255
        
        return self.cvimg_to_imgdata(np.uint8(dst))
    
    def drag_object(self, rect):
        
        tempimg = self.srcimg.copy()
        rect_in_src = (( rect[0][0] * tempimg.shape[1] / self.frame_bitmap_size[0],
                         rect[0][1] * tempimg.shape[0] / self.frame_bitmap_size[1]
                         ),
                       ( rect[1][0] * tempimg.shape[1] / self.frame_bitmap_size[0],
                         rect[1][1] * tempimg.shape[0] / self.frame_bitmap_size[1]
                        )
                       )
        line_width = 3 * tempimg.shape[0] / self.frame_bitmap_size[0]
        cv2.rectangle(tempimg, rect_in_src[0], rect_in_src[1], DRAG_COLOR, line_width)
        self.object_rect = rect_in_src        
        return self.cvimg_to_imgdata(tempimg)
    
    def set_object_template(self):
        lt = (min(self.object_rect[0][0],self.object_rect[1][0]),
              min(self.object_rect[0][1],self.object_rect[1][1])) # left top
        rb = (max(self.object_rect[0][0],self.object_rect[1][0]),
              max(self.object_rect[0][1],self.object_rect[1][1])) # right bottom
        print(lt,rb)
        self.object_template = self.srcimg[ lt[1]:rb[1] , lt[0]:rb[0] ,:]
    
    def match_template(self): 
        methods = ['cv2.TM_CCOEFF', 'cv2.TM_CCOEFF_NORMED', 'cv2.TM_CCORR',
            'cv2.TM_CCORR_NORMED', 'cv2.TM_SQDIFF', 'cv2.TM_SQDIFF_NORMED']
        method = eval(methods[0])
        res = cv2.matchTemplate(self.srcimg, self.object_template, method)
        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)
        
        if method in [cv2.TM_SQDIFF, cv2.TM_SQDIFF_NORMED]:
            tl = min_loc
        else:
            tl = max_loc
            
        br = (tl[0] + self.object_template.shape[1], 
              tl[1] + self.object_template.shape[0]
              )
        
        rst_img = self.srcimg.copy()
        line_width = 3 * rst_img.shape[0] / self.frame_bitmap_size[0]
        cv2.rectangle(rst_img,tl, br, OBJECT_MATCH_COLOR, line_width)
        return self.cvimg_to_imgdata(rst_img)

class WebcamTest(StaticTest):# Need cap.release()
    ''' 摄像头读取测试类 '''
    def __init__(self, frame_bitmap_size):
        self.image_adjust_settings = {'Brightness':50,
                                      'Contrast':50,
                                      'Gamma':50,
                                      }
        # 主窗口中bitmap的可视尺寸
        self.frame_bitmap_size = tuple(frame_bitmap_size)
        
        self.cap = cv2.VideoCapture(0)
        
        _, self.srcimg = self.cap.read()
        
    
    def next(self):
        _, self.srcimg = self.cap.read()
    
    def release_cap(self):
        self.cap.release()



from multiprocessing import Process, Array

# class WebcamService(object):
#     ''' 摄像头读取服务类 '''
#     def __init__(self, frame_bitmap_size):
#         self.frame_bitmap_size = tuple(frame_bitmap_size)
#         self.cap = cv2.VideoCapture(0)
#         _, self.frame = self.cap.read()
#     
#     def get_rsz_frame(self):
#         import time
#         a=time.clock()
#         _, self.frame = self.cap.read()
#         frame = cv2.resize(self.frame, self.frame_bitmap_size, interpolation = cv2.INTER_CUBIC)
#         return frame
#     
#     def get_frame(self):
#         _, self.frame = self.cap.read()
#         return self.frame
#     
#     def release(self):
#         self.cap.release()

class TrackService(StaticTest):
    ''' 目标跟踪服务类（继承静态测试类的一些处理接口） 
    '''
    def __init__(self, frame_bitmap_size):
        self.image_adjust_settings = {'Brightness':50,
                                      'Contrast':50,
                                      'Gamma':50,
                                      }
        # 主窗口中bitmap的可视尺寸
        self.frame_bitmap_size = tuple(frame_bitmap_size)
    
       
    def set_srcimg(self, img):
        self.srcimg = img
        
        
import threading, time
import mmap

class WebcamService(object):
    ''' 摄像头服务类，使用多线程方式防止占用过多的GUI线程处理时间 
                        使用 mmap方式进行通信，速度快  '''
    def __init__(self, frame_bitmap_size):
        mem_tagname = 'cap_mem_buf'
        
        self.capthread = CaptureThread(mem_tagname)
        self.cap_length = self.capthread.get_cap_str_length()
        self.frame = self.capthread.get_example_frame()
        self.frame_shape = self.frame.shape
        self.frame_dtype = self.frame.dtype
        
        self.mmap_file = mmap.mmap(-1, self.cap_length, access = mmap.ACCESS_READ, tagname = mem_tagname)
        
        self.capthread.start()  
        
        #------测试之用--------
        #img_name = r'color\colorcircles.bmp'
        #img_name = r'color\colorruler.jpg'
        #self.testimg = cv2.imread(r'F:\Workplace\GroundStation\imageprocess\%s'%img_name,cv2.IMREAD_COLOR)
    
    def get_frame_size(self):
        return (self.frame_shape[1], self.frame_shape[0])
    
    def mem_string_to_img(self):
        self.mmap_file.seek(0)
        s = self.mmap_file.read(self.cap_length)
        img = np.ndarray(shape = self.frame_shape, dtype = self.frame_dtype, buffer = s)
        self.frame = img
        return img
      
    def get_frame(self):
        #---测试之用--- 
        #return self.testimg
        #-----------
        return self.mem_string_to_img()
    
    def release(self):
        self.capthread.stop()

class CaptureThread(threading.Thread):
    ''' 从摄像头读取数据的线程 '''
    def __init__(self, mem_tagname):
        threading.Thread.__init__(self)
        self.stop_thread = False              
        self.cap = cv2.VideoCapture(1)
        self.cap.read()
        _, self.frame = self.cap.read()
        s = self.frame.tostring()
        self.cap_length = len(s)
        
        self.mmap_file = mmap.mmap(0, self.cap_length, access = mmap.ACCESS_WRITE, tagname = mem_tagname)
        self.mmap_file.write(s)
        
    def get_example_frame(self):  
        return self.frame
    
    def get_cap_str_length(self):
        return self.cap_length
        
    def run(self):
        print('Capture Thread start')
        while not self.stop_thread:
            _, frame = self.cap.read()
            s = frame.tostring()
            self.mmap_file.seek(0)
            self.mmap_file.write(s)
        
        self.mmap_file.close()
        self.cap.release()
        print('Capture Thread end')
    
    def stop(self):
        self.stop_thread = True

  

if __name__ == '__main__':
    x=WebcamService()
    