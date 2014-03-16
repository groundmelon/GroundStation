# -*- coding: utf-8 -*-
import threading
import wx

class SerialReceiver(threading.Thread): #The timer class is derived from the class threading.Thread
    def __init__(self, ser, window):
        threading.Thread.__init__(self)
        self.ser = ser
        self.window = window
        self.thread_stop = False

    def run(self): #Overwrite run() method, put what you want the thread do here
        while not self.thread_stop:
            rcvchr = self.ser.read(1)
            if rcvchr:
                wx.CallAfter(self.window.on_xbee_receive_char,rcvchr)
        print('Serial-Reciver-%s will stop.'%self.getName())
            
    def stop(self):
        self.thread_stop = True
       