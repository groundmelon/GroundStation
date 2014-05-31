# -*- coding: utf-8 -*- 
'''
独立窗口显示

Created on 2014-2-24

@author: Administrator
'''
import wx
import numpy as np
import util
from IndependentImageDisplayBase import IndependentImageDisplayBase
from Definition import DISPLAY_INDEPENDENT_VIDEO

WIDTH_SCALE_BASE = 4.0 #: 宽高比宽度基数
HEIGHT_SCALE_BASE = 3.0 #: 宽高比高度基数

LABEL_TEXT_COLOR = wx.BLUE #: 正常标签颜色
WARNING_TEXT_COLOR = wx.RED #: 警告标签颜色

class VideoDisplayFrame(IndependentImageDisplayBase):
    '''
    独立窗口显示
    '''
    def __init__(self, parent):
        IndependentImageDisplayBase.__init__(self, parent)
        self.SetIcon(wx.Icon(r'resources/gs.ico', wx.BITMAP_TYPE_ICO))
        self.parent = parent
        self.Bind(wx.EVT_CLOSE, self.OnClose)
        self.user_size = (0,0)
        self.dc = wx.ClientDC(self.m_bitmap)
        self.CentreOnScreen()
    
    def on_frame_size_changed(self, event):
        '''
        更新窗口大小
        '''
        self.user_size = self.GetClientSizeTuple()
    
    def OnClose(self, event):
        '''
        关闭独立显示窗口
        '''
        self.parent.remove_work(DISPLAY_INDEPENDENT_VIDEO)
        self.parent.video_window = None
        self.Destroy()
    
#     def update_image_with_info(self, cvimg, info):
#         assert isinstance(cvimg, np.ndarray)       
#         cvimg_size = (cvimg.shape[1], cvimg.shape[0])     
# #        if self.user_size[0] < cvimg_size[0] or self.user_size[1] < cvimg_size[1]:
#         if self.user_size < (200, 200):
#             # user hasn't change window size
#             self.SetClientSizeWH(cvimg_size[0], cvimg_size[1])
#             img_size = cvimg_size
#             img = cvimg
#         else:
#             cli_size = self.GetClientSizeTuple()
#             cli_scale = (float(cli_size[0]/WIDTH_SCALE_BASE),
#                          float(cli_size[1]/HEIGHT_SCALE_BASE)
#                          )
#             if cli_scale[0] > cli_scale[1]:#窗口是扁的
#                 scale = float(cli_size[1])/float(cvimg_size[1])
#                 img = util.cvimg_rescale(cvimg, scale)
#                 img_size = img.shape[1::-1]
#             else:#窗口是高的
#                 scale = float(cli_size[0])/float(cvimg_size[0])
#                 img = util.cvimg_rescale(cvimg, scale)
#                 img_size = img.shape[1::-1]
#         #change m_bitmap size
#         self.m_bitmap.SetSize(img_size)
#         self.m_bitmap.Center()
#         
#         bmp = util.cvimg_to_wxbmp(img)
#         memory = wx.MemoryDC( )
#         memory.SetFont( util.WXFONT )
#         memory.SelectObject( bmp )
#         if self.m_menuItem_osd.IsChecked():
#             text_left_top = (util.PADDING, util.PADDING)
#             # draw info
#             for index, item in enumerate(info):
#                 if item.type == util.InfoEntry.TYPE_LABEL:
#                     memory.SetTextForeground( LABEL_TEXT_COLOR )
#                 elif item.type == util.InfoEntry.TYPE_WARNING:
#                     memory.SetTextForeground( WARNING_TEXT_COLOR )
#                 pos = (text_left_top[0], text_left_top[1]+int(index*util.TEXTSIZE[1]*1.5))
#                 memory.DrawText( str(item), pos[0], pos[1])
#             # draw time
#             memory.SetTextForeground( LABEL_TEXT_COLOR )
#             pos = (img_size[0] - util.PADDING - util.TIME_TEXT_WIDTH,
#                    text_left_top[1])
#             memory.DrawText(util.get_now(), pos[0], pos[1])
#         self.dc.Blit(0, 0, bmp.Size[0], bmp.Size[1], memory, 0, 0)
    
    def update_image(self, wximg, info):
        '''
        更新图像
        @param wximg: 待更新的wx.Image
        @param info: OSD信息，A list of InfoEntry实例
        '''
        img_size = (wximg.GetWidth(), wximg.GetHeight())
        if self.user_size < (200, 200):
            # user hasn't change window size
            self.SetClientSizeWH(img_size[0], img_size[1]) # 按图像大小扩充窗口大小
            cli_size = self.GetClientSizeTuple() # 保存窗口大小
            dst_size = img_size # 保存目标bmp大小
        else:
            # user has customized window size
            cli_size = self.GetClientSizeTuple()
            cli_scale = (float(cli_size[0]/WIDTH_SCALE_BASE),
                         float(cli_size[1]/HEIGHT_SCALE_BASE)
                         ) # 用户自定义大小在宽高方向的比例
            if cli_scale[0] > cli_scale[1]: # 窗口是相对较扁的
                scale = float(cli_size[1])/float(img_size[1]) # 以高度比例为准
            else:# 窗口是相对较高的
                scale = float(cli_size[0])/float(img_size[0]) # 以宽度比例为准
            dst_size = (img_size[0]*scale, img_size[1]*scale) # 保存目标bmp大小
        
        self.m_bitmap.SetSize(dst_size) # 把m_bitmap控件设置为目标bmp大小
        self.m_bitmap.Center() # 控件居中
        
        wxbmp = wx.BitmapFromImage(wximg.Rescale(dst_size[0],dst_size[1])) # 改变wxImage大小，转换成wx.Bitmap
        
        memory = wx.MemoryDC()
        memory.SelectObject(wxbmp)
        memory.SetFont( util.WXFONT )
        if self.m_menuItem_osd.IsChecked():
            text_left_top = (util.PADDING, util.PADDING) # 文字左上角位置
            # draw info
            for index, item in enumerate(info):
                if item.type == util.InfoEntry.TYPE_LABEL:# 正常显示，颜色正常
                    memory.SetTextForeground( LABEL_TEXT_COLOR )
                elif item.type == util.InfoEntry.TYPE_WARNING: # 警报显示，颜色为警报颜色
                    memory.SetTextForeground( WARNING_TEXT_COLOR )
                pos = (text_left_top[0], 
                       text_left_top[1]+int(index*util.TEXTSIZE[1]*1.5)
                       ) # 设置该条目的文字位置
                memory.DrawText( str(item), pos[0], pos[1])
            
            # draw time
            memory.SetTextForeground( LABEL_TEXT_COLOR )
            pos = (dst_size[0] - util.PADDING - util.TIME_TEXT_WIDTH,
                   text_left_top[1]
                   )
            memory.DrawText(util.get_now(), pos[0], pos[1])

        self.dc.Blit(0, 0, cli_size[0], cli_size[1], memory, 0, 0)