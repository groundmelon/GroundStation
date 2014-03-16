# -*- coding: utf-8 -*- 
'''
Created on 2013-12-28

@author: GroundMelon
'''
import wx
from IndependentImageDisplayBase import IndependentImageDisplayBase
from Definition import DISPLAY_INDEPENDENT_VIDEO

WIDTH_PADDING = 16
HEIGHT_PADDING = 38

class IndependentImageDisplayFrame(IndependentImageDisplayBase):
    def __init__(self, parent):
        IndependentImageDisplayBase.__init__(self, parent)
        self.parent = parent
        self.Bind(wx.EVT_CLOSE, self.OnClose)
        self.user_size = (0,0)
        self.dc = wx.ClientDC(self.m_bitmap)
        self.CentreOnScreen()
    
    def update_image(self, bmp):   
        if self.user_size[0] < bmp.Size[0] or self.user_size[1] < bmp.Size[1]:
            # user hasn't change window size
            self.SetSize((bmp.Size[0]+WIDTH_PADDING,bmp.Size[1]+HEIGHT_PADDING))
        self.m_bitmap.SetSize((bmp.Size[0],bmp.Size[1]))
        self.m_bitmap.Center()
        self.dc.DrawBitmap(bmp, 0, 0)
    
    def on_frame_size_changed(self, event):
        self.user_size = self.GetSize()
    
    def OnClose(self, event):
        self.parent.remove_work(DISPLAY_INDEPENDENT_VIDEO)
        self.parent.video_window = None
        self.Destroy()