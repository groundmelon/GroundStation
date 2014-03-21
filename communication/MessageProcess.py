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
PKGTYPE_PID = {'X':0x01, 'Y':0x02, 'Z':0x03}
PKGTYPE_INFO = 0x04
PKGTYPE_LOC = 0x0F
PKGTYPE_SETPID = 0x55





def pack(typ, body):
    return ''.join([SNDHEAD, typ, body, SNDEND])

def packbyte(b):
    return struct.pack('B', b)

def pack_adj_pid_para(para, axis):
    assert len(para) == 3, 'Parameter length error.' 
    typ = packbyte(PKGTYPE_PID[axis])
    body = ''.join([struct.pack('<f',v) for v in para])
    return pack(typ, body)

def pack_get_info():
    typ = packbyte(PKGTYPE_INFO)
    body = '\x01\x00\x00\x00' + '\x00'*16
    return pack(typ, body)

def pack_set_pid_para():
    typ = packbyte(PKGTYPE_SETPID)
    body = ''.join([struct.pack('<iIf',-15,15,1.0)])
    return pack(typ, body)

def unpack(buf):
    rst = struct.unpack('<2B5fB', buf)
    if (rst[0] == RCVHEAD) and (rst[-1] == RCVEND):
        typ = rst[1]
        data = rst[2:-1]
        return (typ, data)
    else:
        return (None, None)