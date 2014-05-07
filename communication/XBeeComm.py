# -*- coding: utf-8 -*- 
'''
XBee通信模块

Created on 2013-12-4

@author: GroundStation
'''
import serial
import serial.tools.list_ports as lstprt
from SerialReceiverThread import SerialReceiver



class XBee(object):
    '''
    XBee通信类
    '''
    def __init__(self, window):
        '''
        初始化
        @param window:用于传递当接收者线程接收到字符时的回调函数 
        '''
        self.window = window
        self.ser = serial.Serial()
        self.rcvbuf = [] #： 接收缓冲
        self.newbuf = [] #： 新接收内容缓冲（用于 append text）
        self.max_buffer_length = 256
    
    def get_supported_info(self):
        '''
        获取可用的串口设置
        @return: 表示设置的字典
        '''       
        info = {}
        info['com'] = [each[0] for each in list(lstprt.comports())]
        info['baudrate'] = sorted(dict(self.ser.getSupportedBaudrates()).keys(),
                                  lambda a,b:cmp(int(a),int(b)))
        info['bytesize'] = dict(self.ser.getSupportedByteSizes()).keys()
        info['parity'] = dict(self.ser.getSupportedParities()).keys()
        info['stopbit'] = dict(self.ser.getSupportedStopbits()).keys()
        return info
    
    def get_com_info(self):
        '''
        获取各个COM口的属性文本
        @return: 表示COM口属性的文本
        '''
        msg = ''
        for each in list(lstprt.comports()):
            msg += "        %s \t %s\n"%(each[0],each[1])
        return msg 
    
    def apply_options(self,option):
        '''
        应用设置
        @param option: 表示设置的字典
        '''        
        self.ser.setBaudrate(option['baudrate'])
        self.ser.setByteSize(option['bytesize'])
        self.ser.setParity(option['parity'])
        self.ser.setStopbits(option['stopbit'])
        self.ser.setXonXoff(option['XonXoff'])
        self.ser.setRtsCts(option['RtsCts'])
        self.ser.setPort(option['com'])
        
    def open(self, options):
        '''
        打开串口
        
            - 应用设置
            - 设置超时(阻塞模式, 参考 U{http://pyserial.sourceforge.net/pyserial_api.html#module-serial})
            - 打开端口
            - 开启接收者线程
        @param option: 表示设置的字典
        '''
        self.apply_options(options)
        self.ser.timeout = 10
        self.ser.open()
        self.receiver = SerialReceiver(self.ser, self.window)
        self.receiver.start()
        print 'Port info:%s'%str(self.ser)
    
    def close(self):
        '''
        关闭XBee
        '''
        self.receiver.stop()
        self.ser.close()
    
    def send_string(self, string):
        '''
        使用XBee发送一个字符串
        @param string: 待发送字符串
        '''
        return self.ser.write(string)
        
    def on_receive_char(self, ch):
        '''
        接收到一个字符的回调函数
        @param ch: 接收的字符
        '''     
        self.rcvbuf.append(ch)
        self.newbuf.append(ch)
        if len(self.rcvbuf) > self.max_buffer_length:
            self.rcvbuf.pop(0)
    
    def get_rcvbuf(self):
        '''
        获取接收缓冲区的内容
        @return: 接收缓冲区的副本
        '''
        return list(self.rcvbuf)
    
    def get_new_buf(self):
        '''
        获取接收缓冲区的新内容
        @return: 新内容的副本
        '''
        temp = list(self.newbuf)
        self.newbuf = list()# 清空new_buf
        return temp
    
    def clear_rcvbuf(self):
        '''
        清除接收缓冲区
        '''
        self.rcvbuf = list()

if __name__ == '__main__':
    xbee=XBee()
    xbee.open({'com'     :   'COM2',
                  'baudrate':   9600,
                  'bytesize':   8,
                  'parity'  :   'N',
                  'stopbit' :   1,
                  'RtsCts':False,#hard flow control
                  'XonXoff':False,#software flow control
                  })
    import time
    time.sleep(200)
    xbee.close()
    