# -*- coding: utf-8 -*- 
'''
Created on 2013-12-4

@author: Administrator
'''
import wx
import PickleFileIO
import os

class MenuBlock():
    def about(self):
        wx.MessageBox(u'GroundStation V1.0\nGroundMelon@gmail.com', u"关于",wx.OK | wx.ICON_INFORMATION)
        
    def save_comm_option(self,options):
        dialog = wx.FileDialog(None, u"保存设置到...", os.getcwd(),
                    u"xbee", u"设置文件 (*.gss)|*.gss", wx.SAVE)
        if dialog.ShowModal() == wx.ID_OK:
            filepath = dialog.GetPath()
            try:
                pfio = PickleFileIO.PickleFileIO(filepath)
                pfio.save(options)
                self.m_statusBar.SetStatusText(u'通信设置"%s"已经保存。'%filepath)
                wx.MessageBox(u'通信设置"%s"已经保存。'%filepath, u"保存成功",wx.OK | wx.ICON_INFORMATION)
            except Exception,e:
                wx.MessageBox(u'通信设置"%s"保存失败。\n%s'%(filepath,str(e)), u"保存失败",wx.OK | wx.ICON_ERROR)
                self.m_statusBar.SetStatusText(u'通信设置"%s"保存发生错误'%filepath)    
        dialog.Destroy()
    
    def load_comm_option(self):
        dialog = wx.FileDialog(None, "读取设置", os.getcwd(),
                    "", u"设置文件 (*.gss)|*.gss", wx.OPEN)
        if dialog.ShowModal() == wx.ID_OK:
            filepath = dialog.GetPath()
            try:
                pfio = PickleFileIO.PickleFileIO(filepath)
                self.comm_options = pfio.load()
                self.m_statusBar.SetStatusText(u'通信设置"%s"已经应用。'%filepath)
                wx.MessageBox(u'通信设置"%s"已经应用。'%filepath, u"设置成功",wx.OK | wx.ICON_INFORMATION)
            except (EOFError,IOError),e:
                wx.MessageBox(u'通信设置"%s"应用失败。\n%s'%(filepath,str(e)), u"设置失败",wx.OK | wx.ICON_ERROR)
                self.m_statusBar.SetStatusText(u'通信设置"%s"应用发生错误'%filepath)    
        dialog.Destroy()
        
    def load_default_comm_options(self):
        # load default settings
        filepath = r'communication\xbee.gss'
        try:
            pfio = PickleFileIO.PickleFileIO(filepath)
            self.comm_options = pfio.load()
            self.m_statusBar.SetStatusText(u'默认通信设置"%s"已经应用。'%filepath)
        except (EOFError,IOError),e:
            self.m_statusBar.SetStatusText(u'未发现默认设置')
    
    def display_comm_option(self, options):
        msg=''
        for (k,v) in options.items():
            msg += '%s \t %s\n'%(k,v)
        wx.MessageBox(msg, u"设置信息",wx.OK | wx.ICON_INFORMATION)