# -*- coding: utf-8 -*-
'''
串口通信接收者线程

Created on 2013-12-4

@author: GroundMelon
'''
import threading
import wx

class SerialReceiver(threading.Thread): #The timer class is derived from the class threading.Thread
    '''
    串口通信接收者线程
    '''
    def __init__(self, ser, window):
        '''
        接收者线程初始化
        @param ser: 串口类,serial.Serial的实例
        @param window:用于传递当接收者线程接收到字符时的回调函数 
        '''
        threading.Thread.__init__(self)
        self.ser = ser
        self.window = window
        self.thread_stop = False

    def run(self): #Overwrite run() method, put what you want the thread do here
        '''
        线程的运行函数，从串口以阻塞方式接收数据
        '''
        while not self.thread_stop:
            rcvchr = self.ser.read(1)
            if rcvchr:
                wx.CallAfter(self.window.on_xbee_receive_char,rcvchr)
        print('Serial-Reciver-%s will stop.'%self.getName())
            
    def stop(self):
        '''
        停止线程
        '''
        self.thread_stop = True
       