'''
Created on 2013-12-4

@author: Administrator
'''
import serial
import serial.tools.list_ports as lstprt
from SerialReceiverThread import SerialReceiver



class XBee(object):
    def __init__(self, window):
        self.window = window
        self.ser = serial.Serial()
        self.rcvbuf = []
        self.newbuf = []
        self.max_buffer_length = 256
    
    def get_supported_info(self):       
        info = {}
        info['com'] = [each[0] for each in list(lstprt.comports())]
        info['baudrate'] = sorted(dict(self.ser.getSupportedBaudrates()).keys(),
                                  lambda a,b:cmp(int(a),int(b)))
        info['bytesize'] = dict(self.ser.getSupportedByteSizes()).keys()
        info['parity'] = dict(self.ser.getSupportedParities()).keys()
        info['stopbit'] = dict(self.ser.getSupportedStopbits()).keys()
        return info
    
    def get_com_info(self):
        msg = ''
        for each in list(lstprt.comports()):
            msg += "        %s \t %s\n"%(each[0],each[1])
        return msg 
    
    def apply_options(self,option):        
        self.ser.setBaudrate(option['baudrate'])
        self.ser.setByteSize(option['bytesize'])
        self.ser.setParity(option['parity'])
        self.ser.setStopbits(option['stopbit'])
        self.ser.setXonXoff(option['XonXoff'])
        self.ser.setRtsCts(option['RtsCts'])
        self.ser.setPort(option['com'])
        
    def open(self, options):
        self.apply_options(options)
        self.ser.timeout = 10
        self.ser.open()
        self.receiver = SerialReceiver(self.ser, self.window)
        self.receiver.start()
        print 'Port info:%s'%str(self.ser)
    
    def close(self):
        self.receiver.stop()
        self.ser.close()
    
    def send_string(self, string):
        return self.ser.write(string)
        
    def on_receive_char(self, ch):     
        self.rcvbuf.append(ch)
        self.newbuf.append(ch)
        if len(self.rcvbuf) > self.max_buffer_length:
            self.rcvbuf.pop(0)
    
    def get_rcvbuf(self):
        return self.rcvbuf
    
    def get_new_buf(self):
        temp = self.newbuf
        self.newbuf = []
        return temp
    
    def clear_rcvbuf(self):
        self.rcvbuf = []

if __name__ == '__main__':
    xbee=XBee()
    xbee.open({'com'     :   'COM7',
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
    