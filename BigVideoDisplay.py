# -*- coding: utf-8 -*- 
'''
Created on 2014-2-24

@author: Administrator
'''
import wx
import numpy as np
import util
from IndependentImageDisplayBase import IndependentImageDisplayBase
from Definition import DISPLAY_INDEPENDENT_VIDEO

WIDTH_SCALE_BASE = 4.0
HEIGHT_SCALE_BASE = 3.0
PADDING = 10
TEXTSIZE = 12

LABEL_TEXT_COLOR = wx.BLUE
WARNING_TEXT_COLOR = wx.RED

class VideoDisplayFrame(IndependentImageDisplayBase):
    def __init__(self, parent):
        IndependentImageDisplayBase.__init__(self, parent)
        self.parent = parent
        self.Bind(wx.EVT_CLOSE, self.OnClose)
        self.user_size = (0,0)
        self.dc = wx.ClientDC(self.m_bitmap)
        self.CentreOnScreen()
        self.font = wx.Font( TEXTSIZE, 74, 90, 90, False, "Consolas" )
    
    def refresh_size(self, bmpSize):   
        pass
        #self.dc.DrawBitmap(bmp, 0, 0)
    
    def on_frame_size_changed(self, event):
        self.user_size = self.GetClientSizeTuple()
    
    def OnClose(self, event):
        self.parent.remove_work(DISPLAY_INDEPENDENT_VIDEO)
        self.parent.video_window = None
        self.Destroy()
    
    def update_image_with_info(self, cvimg, info):
        assert isinstance(cvimg, np.ndarray)       
        cvimg_size = (cvimg.shape[1], cvimg.shape[0])     
#        if self.user_size[0] < cvimg_size[0] or self.user_size[1] < cvimg_size[1]:
        if self.user_size < (200, 200):
            # user hasn't change window size
            self.SetClientSizeWH(cvimg_size[0], cvimg_size[1])
            img_size = cvimg_size
            img = cvimg
        else:
            cli_size = self.GetClientSizeTuple()
            cli_scale = (float(cli_size[0]/WIDTH_SCALE_BASE),
                         float(cli_size[1]/HEIGHT_SCALE_BASE)
                         )
            if cli_scale[0] > cli_scale[1]:#窗口是扁的
                scale = float(cli_size[1])/float(cvimg_size[1])
                img = util.cvimg_rescale(cvimg, scale)
                img_size = img.shape[1::-1]
            else:#窗口是高的
                scale = float(cli_size[0])/float(cvimg_size[0])
                img = util.cvimg_rescale(cvimg, scale)
                img_size = img.shape[1::-1]
        #change m_bitmap size
        self.m_bitmap.SetSize(img_size)
        self.m_bitmap.Center()
        
        bmp = util.cvimg_to_wxbmp(img)
        memory = wx.MemoryDC( )
        memory.SetFont( self.font )
        memory.SelectObject( bmp )
        text_left_bottom = (PADDING, PADDING + TEXTSIZE)
        for index, item in enumerate(info):
            if item.type == util.InfoEntry.TYPE_LABEL:
                memory.SetTextForeground( LABEL_TEXT_COLOR )
            elif item.type == util.InfoEntry.TYPE_WARNING:
                memory.SetTextForeground( WARNING_TEXT_COLOR )
            pos = (text_left_bottom[0], text_left_bottom[1]+int(index*TEXTSIZE*1.5))
            memory.DrawText( str(item), pos[0], pos[1])
        self.dc.Blit(0, 0, bmp.Size[0], bmp.Size[1], memory, 0, 0)
        