# -*- coding: utf-8 -*- 
'''
通信消息包的相关处理

Created on 2014-3-20

@author: GroundMelon
'''
import struct

SNDHEAD = struct.pack('B', 0xFF)#: 通信数据发送包头
SNDEND = struct.pack('B', 0xAA)#: 通信数据发送包尾
RCVHEAD = struct.pack('B', 0xFF)#: 通信数据接收包头
RCVEND = struct.pack('B', 0xAA)#: 通信数据接收包尾

# ---- Send Msg Type ID ----
PKGTYPE_PID = {'X':0x01, 'Y':0x02, 'Z':0x03, 'H':0x04, 'P':0x05}#: 包类型定义： 各轴PID参数
PKGTYPE_INVALID = 0x00

PKGTYPE_REF = 0x06 #: 包类型定义：给定
PKGTYPE_U0 = 0x07 #: 包类型定义：控制量 pitch P,I,D roll P,I
PKGTYPE_U1 = 0x08 #: 包类型定义：控制量 roll D, yaw P,I,D 
PKGTYPE_PT = 0x09 #: 包类型定义：Pan/Tilt camera control
PKGTYPE_CTRL = 0x0A #: 包类型定义：控制状态
PKGTYPE_ATTI = 0x0B #: 包类型定义：姿态高度电压状态信息
PKGTYPE_POS = 0x0C #： 包类型定义：位置信息
PKGTYPE_SETPID = 0x0D #： 包类型定义：固定PID参数
PKGTYPE_GETPID = 0x0E #： 包类型定义：获取PID参数
PKGTYPE_LOC = 0x0F # invalid






def pack(typ, body):
    '''
    打包一帧消息
    @param typ: 包类型
    @param body: 包内容
    @return: 完整地一包数据
    '''
    rtn = ''.join([SNDHEAD, typ, body, SNDEND])
    assert len(rtn) == 23
    return rtn

def packbyte(b):
    return struct.pack('B', b)

def pack_adj_pid_para(para, axis):
    '''
    调参命令打包
    @param para: 参数内容
    @param axis: 参数所属轴向
    @return: 完整地一包数据
    '''
    assert len(para) == 4, 'Parameter length error.' # P I D SpeedP
    typ = packbyte(PKGTYPE_PID[axis])
    body = ''.join([struct.pack('<f',v) for v in para])
    body = ''.join([body, '\x00'*4])
    return pack(typ, body)

def pack_set_pid():
    '''
    固定PID参数命令打包
    @return: 完整地一包数据
    '''
    typ = packbyte(PKGTYPE_SETPID)
    body = ''.join(['\x00'*4*5])
    return pack(typ, body)

def pack_get_pid():
    '''
    获取PID参数命令打包
    @return: 完整地一包数据
    '''
    typ = packbyte(PKGTYPE_GETPID)
    body = ''.join(['\x00'*4*5])
    return pack(typ, body)

# def pack_get_info():
#     typ = packbyte(PKGTYPE_INFO)
#     body = '\x00'*4*5
#     return pack(typ, body)

def pack_control(ctrltype=0, smart_direction=0, p=0, r=0, y=0, t=0):
    '''
    控制状态命令打包
    @param ctrltype: 0 遥控器控制 ；1 摇杆控制
    @param smart_direction: 0关1开
    @return: 完整地一包数据
    '''
    typ = packbyte(PKGTYPE_CTRL)
    body = struct.pack('BBBB', ctrltype, 0, 0, smart_direction)
    body = ''.join([body, struct.pack('<ffff', r, p, y, t)])
    return pack(typ, body)

def pack_pt(p, r):
    '''
    云台控制命令打包
    @param p: 云台pitch
    @param r: 云台roll
    @return: 完整地一包数据
    '''
    typ = packbyte(PKGTYPE_PT)
    body = ''.join([struct.pack('<ff', p, r),'\x00'*4*3])
    return pack(typ, body)

    
def unpack_type(buf):
    '''
   解包，验证包头包尾，解出包类型
   @return: 数据包有效(类型，数据) 数据包无效(None,None)
    '''
    rst = struct.unpack('<BB20sB', buf)
    if (rst[0] == ord(RCVHEAD)) and (rst[3] == ord(RCVEND)):
        typ = rst[1]
        data = rst[2]
        return (typ, data)
    else:
        return (None, None)

def unpack_ctrl(buf):
    '''
    按控制包的类型解包，16Bf
    @return: 解包结果的tuple
    '''
    rst = struct.unpack('<16Bf', buf)
    return rst

def unpack(buf):
    '''
    按5个float解包
    '''
    return unpack_5f(buf)
#     rst = struct.unpack('<2B5fB', buf)
#     if (rst[0] == RCVHEAD) and (rst[-1] == RCVEND):
#         typ = rst[1]
#         data = rst[2:-1]
#         return (typ, data)
#     else:
#         return (None, None)

def unpack_5f(buf):
    '''
    按5个float解包
    '''
    return struct.unpack('<5f', buf)