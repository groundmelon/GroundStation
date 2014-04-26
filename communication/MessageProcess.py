# -*- coding: utf-8 -*- 
'''
Created on 2014-3-20

@author: GroundMelon
'''
import struct

SNDHEAD = struct.pack('B', 0xFF)
SNDEND = struct.pack('B', 0xAA)
RCVHEAD = 0xFF
RCVEND = 0xAA

# ---- Send Msg Type ID ----
PKGTYPE_PID = {'X':0x01, 'Y':0x02, 'Z':0x03, 'H':0x04, 'P':0x05}
PKGTYPE_INVALID = 0x00

PKGTYPE_REF = 0x06
PKGTYPE_U0 = 0x07 # U pitch P,I,D roll P,I
PKGTYPE_U1 = 0x08 # roll D, MOTOR,AutoHeight,SmartDirection,UAVTIME
PKGTYPE_PT = 0x09 # Pan/Tilt camera control
PKGTYPE_CTRL = 0x0A # Control information
PKGTYPE_ATTI = 0x0B # Attitude information
PKGTYPE_POS = 0x0C # Position information
PKGTYPE_LOC = 0x0F # invalid
PKGTYPE_SETPID = 0x55 # invalid





def pack(typ, body):
    rtn = ''.join([SNDHEAD, typ, body, SNDEND])
    assert len(rtn) == 23
    return rtn

def packbyte(b):
    return struct.pack('B', b)

def pack_adj_pid_para(para, axis):
    assert len(para) == 4, 'Parameter length error.' 
    typ = packbyte(PKGTYPE_PID[axis])
    body = ''.join([struct.pack('<f',v) for v in para])
    body = ''.join([body, '\x00'*4])
    return pack(typ, body)

# def pack_get_info():
#     typ = packbyte(PKGTYPE_INFO)
#     body = '\x00'*4*5
#     return pack(typ, body)

def pack_control(ctrltype=0, smart_direction=0, p=0, r=0, y=0, t=0):
    typ = packbyte(PKGTYPE_CTRL)
    body = struct.pack('BBBB', ctrltype, 0, 0, smart_direction)
    body = ''.join([body, struct.pack('<ffff', r, p, y, t)])
    return pack(typ, body)

def pack_set_pid_para():
    typ = packbyte(PKGTYPE_SETPID)
    body = ''.join([struct.pack('<iIf',-15,15,1.0)])
    return pack(typ, body)

def pack_pt(p, r):
    typ = packbyte(PKGTYPE_PT)
    body = ''.join([struct.pack('<ff', p, r),'\x00'*4*3])
    return pack(typ, body)

    
def unpack(buf):
    return unpack_5f(buf)
#     rst = struct.unpack('<2B5fB', buf)
#     if (rst[0] == RCVHEAD) and (rst[-1] == RCVEND):
#         typ = rst[1]
#         data = rst[2:-1]
#         return (typ, data)
#     else:
#         return (None, None)

def unpack_5f(buf):
    return struct.unpack('<5f', buf)

def unpack_type(buf):
    rst = struct.unpack('<BB20sB', buf)
    if (rst[0] == RCVHEAD) and (rst[3] == RCVEND):
        typ = rst[1]
        data = rst[2]
        return (typ, data)
    else:
        return (None, None)

def unpack_ctrl(buf):
    rst = struct.unpack('<16Bf', buf)
    return rst