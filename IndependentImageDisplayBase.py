# -*- coding: utf-8 -*- 

###########################################################################
## Python code generated with wxFormBuilder (version Sep  8 2010)
## http://www.wxformbuilder.org/
##
## PLEASE DO "NOT" EDIT THIS FILE!
###########################################################################

import wx

###########################################################################
## Class IndependentImageDisplayBase
###########################################################################

class IndependentImageDisplayBase ( wx.Frame ):
	
	def __init__( self, parent ):
		wx.Frame.__init__ ( self, parent, id = wx.ID_ANY, title = u"Display Window", pos = wx.DefaultPosition, size = wx.Size( -1,-1 ), style = wx.DEFAULT_FRAME_STYLE|wx.CLIP_CHILDREN|wx.TAB_TRAVERSAL )
		
		self.SetSizeHintsSz( wx.DefaultSize, wx.DefaultSize )
		
		bSizer = wx.BoxSizer( wx.VERTICAL )
		
		self.m_bitmap = wx.StaticBitmap( self, wx.ID_ANY, wx.NullBitmap, wx.DefaultPosition, wx.DefaultSize, wx.CLIP_CHILDREN )
		bSizer.Add( self.m_bitmap, 0, wx.ALIGN_CENTER|wx.EXPAND, 0 )
		
		self.SetSizer( bSizer )
		self.Layout()
		bSizer.Fit( self )
		
		self.Centre( wx.BOTH )
		
		# Connect Events
		self.Bind( wx.EVT_SIZE, self.on_frame_size_changed )
		self.m_bitmap.Bind( wx.EVT_MOUSEWHEEL, self.on_mouse_wheel )
	
	def __del__( self ):
		pass
	
	
	# Virtual event handlers, overide them in your derived class
	def on_frame_size_changed( self, event ):
		event.Skip()
	
	def on_mouse_wheel( self, event ):
		event.Skip()
	

