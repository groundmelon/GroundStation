# -*- coding: utf-8 -*- 

###########################################################################
## Python code generated with wxFormBuilder (version Sep  8 2010)
## http://www.wxformbuilder.org/
##
## PLEASE DO "NOT" EDIT THIS FILE!
###########################################################################

import wx

###########################################################################
## Class FrameGroundStationBase
###########################################################################

class FrameGroundStationBase ( wx.Frame ):
	
	def __init__( self, parent ):
		wx.Frame.__init__ ( self, parent, id = wx.ID_ANY, title = u"GroundStation", pos = wx.DefaultPosition, size = wx.Size( 800,600 ), style = wx.DEFAULT_FRAME_STYLE|wx.CLIP_CHILDREN|wx.TAB_TRAVERSAL )
		
		self.SetSizeHintsSz( wx.DefaultSize, wx.DefaultSize )
		
		bSizer2 = wx.BoxSizer( wx.VERTICAL )
		
		self.m_panel2 = wx.Panel( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
		bSizer3 = wx.BoxSizer( wx.VERTICAL )
		
		bSizer4 = wx.BoxSizer( wx.HORIZONTAL )
		
		bSizer6 = wx.BoxSizer( wx.VERTICAL )
		
		gSizer2 = wx.GridSizer( 5, 1, 0, 0 )
		
		self.m_button_xbee_option = wx.Button( self.m_panel2, wx.ID_ANY, u"XBee通信设置", wx.DefaultPosition, wx.Size( 100,-1 ), 0 )
		gSizer2.Add( self.m_button_xbee_option, 0, wx.ALIGN_CENTER|wx.ALL, 5 )
		
		self.m_button_toggle_xbee = wx.Button( self.m_panel2, wx.ID_ANY, u"开始Xbee通信", wx.DefaultPosition, wx.Size( 100,-1 ), 0 )
		gSizer2.Add( self.m_button_toggle_xbee, 0, wx.ALIGN_CENTER|wx.ALL, 5 )
		
		self.m_button_video_comm_option = wx.Button( self.m_panel2, wx.ID_ANY, u"图传通信设置", wx.DefaultPosition, wx.Size( 100,-1 ), 0 )
		gSizer2.Add( self.m_button_video_comm_option, 0, wx.ALIGN_CENTER|wx.ALL, 5 )
		
		self.m_button_toggle_video = wx.Button( self.m_panel2, wx.ID_ANY, u"开始图像传输", wx.DefaultPosition, wx.Size( 100,-1 ), 0 )
		gSizer2.Add( self.m_button_toggle_video, 0, wx.ALIGN_CENTER|wx.ALL, 5 )
		
		bSizer6.Add( gSizer2, 1, wx.EXPAND, 5 )
		
		bSizer4.Add( bSizer6, 1, wx.EXPAND, 5 )
		
		bSizer7 = wx.BoxSizer( wx.HORIZONTAL )
		
		bSizer271 = wx.BoxSizer( wx.VERTICAL )
		
		self.m_bitmap_attitude = wx.StaticBitmap( self.m_panel2, wx.ID_ANY, wx.NullBitmap, wx.DefaultPosition, wx.Size( 100,100 ), 0 )
		bSizer271.Add( self.m_bitmap_attitude, 0, wx.ALIGN_CENTER|wx.ALL, 5 )
		
		bSizer7.Add( bSizer271, 1, wx.EXPAND, 5 )
		
		gSizer4 = wx.GridSizer( 2, 2, 0, 0 )
		
		self.m_staticText11 = wx.StaticText( self.m_panel2, wx.ID_ANY, u"高度", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText11.Wrap( -1 )
		gSizer4.Add( self.m_staticText11, 0, wx.ALIGN_RIGHT|wx.ALL, 5 )
		
		self.m_staticText_height = wx.StaticText( self.m_panel2, wx.ID_ANY, u"000.0m", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText_height.Wrap( -1 )
		gSizer4.Add( self.m_staticText_height, 0, wx.ALIGN_LEFT|wx.ALL, 5 )
		
		self.m_staticText12 = wx.StaticText( self.m_panel2, wx.ID_ANY, u"电压", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText12.Wrap( -1 )
		gSizer4.Add( self.m_staticText12, 0, wx.ALIGN_RIGHT|wx.ALL, 5 )
		
		self.m_staticText_vol = wx.StaticText( self.m_panel2, wx.ID_ANY, u"00.0v", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText_vol.Wrap( -1 )
		gSizer4.Add( self.m_staticText_vol, 0, wx.ALIGN_LEFT|wx.ALL, 5 )
		
		self.m_staticText15 = wx.StaticText( self.m_panel2, wx.ID_ANY, u"俯仰", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText15.Wrap( -1 )
		gSizer4.Add( self.m_staticText15, 0, wx.ALIGN_RIGHT|wx.ALL, 5 )
		
		self.m_staticText_pitch = wx.StaticText( self.m_panel2, wx.ID_ANY, u"0d", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText_pitch.Wrap( -1 )
		gSizer4.Add( self.m_staticText_pitch, 0, wx.ALIGN_LEFT|wx.ALL, 5 )
		
		self.m_staticText17 = wx.StaticText( self.m_panel2, wx.ID_ANY, u"横滚", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText17.Wrap( -1 )
		gSizer4.Add( self.m_staticText17, 0, wx.ALIGN_RIGHT|wx.ALL, 5 )
		
		self.m_staticText_roll = wx.StaticText( self.m_panel2, wx.ID_ANY, u"0d", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText_roll.Wrap( -1 )
		gSizer4.Add( self.m_staticText_roll, 0, wx.ALIGN_LEFT|wx.ALL, 5 )
		
		self.m_staticText19 = wx.StaticText( self.m_panel2, wx.ID_ANY, u"偏航", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText19.Wrap( -1 )
		gSizer4.Add( self.m_staticText19, 0, wx.ALIGN_RIGHT|wx.ALL, 5 )
		
		self.m_staticText_yaw = wx.StaticText( self.m_panel2, wx.ID_ANY, u"0d", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText_yaw.Wrap( -1 )
		gSizer4.Add( self.m_staticText_yaw, 0, wx.ALIGN_LEFT|wx.ALL, 5 )
		
		bSizer7.Add( gSizer4, 1, wx.EXPAND, 5 )
		
		bSizer4.Add( bSizer7, 1, wx.EXPAND, 5 )
		
		bSizer3.Add( bSizer4, 1, wx.EXPAND, 5 )
		
		bSizer5 = wx.BoxSizer( wx.HORIZONTAL )
		
		self.m_notebook1 = wx.Notebook( self.m_panel2, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_panel_comm = wx.Panel( self.m_notebook1, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
		self.m_panel_comm.SetBackgroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_BTNFACE ) )
		
		bSizer8 = wx.BoxSizer( wx.VERTICAL )
		
		bSizer9 = wx.BoxSizer( wx.VERTICAL )
		
		self.m_staticText7 = wx.StaticText( self.m_panel_comm, wx.ID_ANY, u"接收区", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText7.Wrap( -1 )
		bSizer9.Add( self.m_staticText7, 0, wx.ALL, 5 )
		
		self.m_textCtrl_comm_receive = wx.TextCtrl( self.m_panel_comm, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, wx.TE_MULTILINE|wx.TE_WORDWRAP )
		self.m_textCtrl_comm_receive.SetMinSize( wx.Size( 400,160 ) )
		
		bSizer9.Add( self.m_textCtrl_comm_receive, 0, wx.ALIGN_CENTER_HORIZONTAL|wx.ALL|wx.EXPAND, 5 )
		
		bSizer14 = wx.BoxSizer( wx.HORIZONTAL )
		
		bSizer21 = wx.BoxSizer( wx.VERTICAL )
		
		bSizer14.Add( bSizer21, 1, wx.EXPAND, 5 )
		
		bSizer19 = wx.BoxSizer( wx.VERTICAL )
		
		m_choice_recv_styleChoices = [ u"ASCII", u"HEX" ]
		self.m_choice_recv_style = wx.Choice( self.m_panel_comm, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, m_choice_recv_styleChoices, 0 )
		self.m_choice_recv_style.SetSelection( 0 )
		bSizer19.Add( self.m_choice_recv_style, 0, wx.ALL|wx.EXPAND, 5 )
		
		bSizer14.Add( bSizer19, 1, wx.EXPAND, 5 )
		
		bSizer20 = wx.BoxSizer( wx.VERTICAL )
		
		self.m_button_recv_clear = wx.Button( self.m_panel_comm, wx.ID_ANY, u"清除接收缓冲区", wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer20.Add( self.m_button_recv_clear, 0, wx.ALL|wx.EXPAND, 5 )
		
		bSizer14.Add( bSizer20, 1, wx.EXPAND, 5 )
		
		bSizer9.Add( bSizer14, 1, wx.EXPAND, 5 )
		
		bSizer8.Add( bSizer9, 4, wx.EXPAND, 5 )
		
		bSizer11 = wx.BoxSizer( wx.VERTICAL )
		
		self.m_staticText8 = wx.StaticText( self.m_panel_comm, wx.ID_ANY, u"发送区", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText8.Wrap( -1 )
		bSizer11.Add( self.m_staticText8, 0, wx.ALL, 5 )
		
		bSizer13 = wx.BoxSizer( wx.VERTICAL )
		
		self.m_textCtrl_comm_send = wx.TextCtrl( self.m_panel_comm, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.Size( -1,-1 ), wx.TE_PROCESS_ENTER )
		bSizer13.Add( self.m_textCtrl_comm_send, 1, wx.ALL|wx.EXPAND, 5 )
		
		bSizer15 = wx.BoxSizer( wx.HORIZONTAL )
		
		bSizer16 = wx.BoxSizer( wx.VERTICAL )
		
		bSizer15.Add( bSizer16, 1, wx.EXPAND, 5 )
		
		bSizer17 = wx.BoxSizer( wx.VERTICAL )
		
		m_choice_send_styleChoices = [ u"ASCII", u"HEX" ]
		self.m_choice_send_style = wx.Choice( self.m_panel_comm, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, m_choice_send_styleChoices, 0 )
		self.m_choice_send_style.SetSelection( 0 )
		bSizer17.Add( self.m_choice_send_style, 0, wx.ALL|wx.EXPAND, 5 )
		
		bSizer15.Add( bSizer17, 1, wx.EXPAND, 5 )
		
		bSizer18 = wx.BoxSizer( wx.VERTICAL )
		
		self.m_button_comm_send = wx.Button( self.m_panel_comm, wx.ID_ANY, u"发送指令", wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer18.Add( self.m_button_comm_send, 0, wx.ALIGN_RIGHT|wx.ALL|wx.EXPAND, 5 )
		
		self.m_checkBox_sent_clear = wx.CheckBox( self.m_panel_comm, wx.ID_ANY, u"发送后清空", wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer18.Add( self.m_checkBox_sent_clear, 0, wx.ALIGN_CENTER_HORIZONTAL|wx.ALL, 5 )
		
		bSizer15.Add( bSizer18, 1, wx.EXPAND, 5 )
		
		bSizer13.Add( bSizer15, 2, wx.EXPAND, 5 )
		
		bSizer11.Add( bSizer13, 1, wx.EXPAND, 5 )
		
		bSizer8.Add( bSizer11, 2, wx.EXPAND, 5 )
		
		self.m_panel_comm.SetSizer( bSizer8 )
		self.m_panel_comm.Layout()
		bSizer8.Fit( self.m_panel_comm )
		self.m_notebook1.AddPage( self.m_panel_comm, u"通信数据查看", True )
		self.m_panel_track = wx.Panel( self.m_notebook1, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
		self.m_panel_track.SetBackgroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_BTNFACE ) )
		self.m_panel_track.Enable( False )
		
		bSizer201 = wx.BoxSizer( wx.VERTICAL )
		
		self.m_bitmap_track = wx.StaticBitmap( self.m_panel_track, wx.ID_ANY, wx.Bitmap( u"resources/null.bmp", wx.BITMAP_TYPE_ANY ), wx.DefaultPosition, wx.Size( 320,240 ), 0 )
		bSizer201.Add( self.m_bitmap_track, 0, wx.ALIGN_CENTER_HORIZONTAL|wx.ALL, 5 )
		
		bSizer211 = wx.BoxSizer( wx.HORIZONTAL )
		
		bSizer23 = wx.BoxSizer( wx.VERTICAL )
		
		m_radioBox_image_adjChoices = [ u"Brightness", u"Contrast", u"Gamma" ]
		self.m_radioBox_image_adj = wx.RadioBox( self.m_panel_track, wx.ID_ANY, u"Adjust", wx.DefaultPosition, wx.DefaultSize, m_radioBox_image_adjChoices, 1, wx.RA_SPECIFY_COLS )
		self.m_radioBox_image_adj.SetSelection( 0 )
		bSizer23.Add( self.m_radioBox_image_adj, 0, wx.ALL, 5 )
		
		bSizer211.Add( bSizer23, 1, wx.EXPAND, 5 )
		
		bSizer24 = wx.BoxSizer( wx.VERTICAL )
		
		bSizer25 = wx.BoxSizer( wx.HORIZONTAL )
		
		self.m_staticText_adjust_type = wx.StaticText( self.m_panel_track, wx.ID_ANY, u"Brightness", wx.DefaultPosition, wx.Size( 60,-1 ), 0 )
		self.m_staticText_adjust_type.Wrap( -1 )
		bSizer25.Add( self.m_staticText_adjust_type, 0, wx.ALIGN_CENTER|wx.ALL, 5 )
		
		self.m_slider_adjust = wx.Slider( self.m_panel_track, wx.ID_ANY, 50, 0, 100, wx.DefaultPosition, wx.Size( 200,40 ), wx.SL_HORIZONTAL|wx.SL_LABELS )
		bSizer25.Add( self.m_slider_adjust, 0, wx.ALIGN_CENTER, 5 )
		
		bSizer24.Add( bSizer25, 1, wx.EXPAND, 5 )
		
		bSizer26 = wx.BoxSizer( wx.HORIZONTAL )
		
		self.m_button_track_image_show = wx.Button( self.m_panel_track, wx.ID_ANY, u"独立窗口", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_button_track_image_show.Enable( False )
		self.m_button_track_image_show.Hide()
		
		bSizer26.Add( self.m_button_track_image_show, 0, wx.ALL, 5 )
		
		gSizer3 = wx.GridSizer( 2, 3, 0, 0 )
		
		self.m_button_toggle_track_video = wx.Button( self.m_panel_track, wx.ID_ANY, u"显示视频", wx.DefaultPosition, wx.DefaultSize, 0 )
		gSizer3.Add( self.m_button_toggle_track_video, 0, wx.ALL, 5 )
		
		self.m_button_select_object = wx.Button( self.m_panel_track, wx.ID_ANY, u"框选目标", wx.DefaultPosition, wx.DefaultSize, 0 )
		gSizer3.Add( self.m_button_select_object, 0, wx.ALL, 5 )
		
		self.m_button_toggle_track = wx.Button( self.m_panel_track, wx.ID_ANY, u"开始追踪", wx.DefaultPosition, wx.DefaultSize, 0 )
		gSizer3.Add( self.m_button_toggle_track, 0, wx.ALL, 5 )
		
		m_choice_track_modeChoices = [ u"template", u"color", u"colormsk" ]
		self.m_choice_track_mode = wx.Choice( self.m_panel_track, wx.ID_ANY, wx.DefaultPosition, wx.Size( 75,-1 ), m_choice_track_modeChoices, 0 )
		self.m_choice_track_mode.SetSelection( 0 )
		gSizer3.Add( self.m_choice_track_mode, 0, wx.ALL, 5 )
		
		bSizer26.Add( gSizer3, 1, wx.EXPAND, 5 )
		
		bSizer24.Add( bSizer26, 2, wx.EXPAND, 5 )
		
		bSizer211.Add( bSizer24, 3, wx.EXPAND, 5 )
		
		bSizer201.Add( bSizer211, 1, wx.TOP, 7 )
		
		self.m_panel_track.SetSizer( bSizer201 )
		self.m_panel_track.Layout()
		bSizer201.Fit( self.m_panel_track )
		self.m_notebook1.AddPage( self.m_panel_track, u"目标跟踪", False )
		self.m_panel_route = wx.Panel( self.m_notebook1, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
		self.m_panel_route.SetBackgroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_BTNFACE ) )
		
		self.m_notebook1.AddPage( self.m_panel_route, u"路径规划", False )
		
		bSizer5.Add( self.m_notebook1, 1, wx.EXPAND |wx.ALL, 5 )
		
		self.m_notebook2 = wx.Notebook( self.m_panel2, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_notebook2.SetBackgroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_BTNFACE ) )
		
		self.m_panel_image = wx.Panel( self.m_notebook2, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
		self.m_panel_image.SetBackgroundColour( wx.Colour( 240, 240, 240 ) )
		
		bSizer27 = wx.BoxSizer( wx.VERTICAL )
		
		self.m_bitmap_video = wx.StaticBitmap( self.m_panel_image, wx.ID_ANY, wx.Bitmap( u"resources/null.bmp", wx.BITMAP_TYPE_ANY ), wx.DefaultPosition, wx.Size( 320,240 ), wx.CLIP_CHILDREN )
		bSizer27.Add( self.m_bitmap_video, 0, wx.ALIGN_CENTER|wx.ALL, 5 )
		
		self.m_button_video_window_show = wx.Button( self.m_panel_image, wx.ID_ANY, u"独立窗口", wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer27.Add( self.m_button_video_window_show, 0, wx.ALIGN_CENTER_HORIZONTAL|wx.ALL, 5 )
		
		self.m_staticText13 = wx.StaticText( self.m_panel_image, wx.ID_ANY, u"MyLabel", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText13.Wrap( -1 )
		self.m_staticText13.SetFont( wx.Font( 10, 74, 90, 90, False, "Consolas" ) )
		
		bSizer27.Add( self.m_staticText13, 0, wx.ALL, 5 )
		
		self.m_panel_image.SetSizer( bSizer27 )
		self.m_panel_image.Layout()
		bSizer27.Fit( self.m_panel_image )
		self.m_notebook2.AddPage( self.m_panel_image, u"实时图像", False )
		
		bSizer5.Add( self.m_notebook2, 1, wx.EXPAND |wx.ALL, 5 )
		
		bSizer3.Add( bSizer5, 3, wx.EXPAND, 0 )
		
		self.m_panel2.SetSizer( bSizer3 )
		self.m_panel2.Layout()
		bSizer3.Fit( self.m_panel2 )
		bSizer2.Add( self.m_panel2, 1, wx.EXPAND |wx.ALL, 0 )
		
		self.SetSizer( bSizer2 )
		self.Layout()
		self.m_menubar1 = wx.MenuBar( 0 )
		self.m_menu_file = wx.Menu()
		self.m_menuItem_save_comm_option = wx.MenuItem( self.m_menu_file, wx.ID_ANY, u"保存通信设置(&S)", wx.EmptyString, wx.ITEM_NORMAL )
		self.m_menu_file.AppendItem( self.m_menuItem_save_comm_option )
		
		self.m_menuItem_load_comm_option = wx.MenuItem( self.m_menu_file, wx.ID_ANY, u"读取通信设置(&L)", wx.EmptyString, wx.ITEM_NORMAL )
		self.m_menu_file.AppendItem( self.m_menuItem_load_comm_option )
		
		self.m_menuItem_check_comm_option = wx.MenuItem( self.m_menu_file, wx.ID_ANY, u"查看通信设置(&C)", wx.EmptyString, wx.ITEM_NORMAL )
		self.m_menu_file.AppendItem( self.m_menuItem_check_comm_option )
		
		self.m_menu_file.AppendSeparator()
		
		self.m_menuItem_exit = wx.MenuItem( self.m_menu_file, wx.ID_ANY, u"退出(&E)", wx.EmptyString, wx.ITEM_NORMAL )
		self.m_menu_file.AppendItem( self.m_menuItem_exit )
		
		self.m_menubar1.Append( self.m_menu_file, u"文件(&F)" ) 
		
		self.m_menu_help = wx.Menu()
		self.m_menuItem_about = wx.MenuItem( self.m_menu_help, wx.ID_ANY, u"关于(&A)", wx.EmptyString, wx.ITEM_NORMAL )
		self.m_menu_help.AppendItem( self.m_menuItem_about )
		
		self.m_menubar1.Append( self.m_menu_help, u"帮助(&H)" ) 
		
		self.SetMenuBar( self.m_menubar1 )
		
		self.m_statusBar = self.CreateStatusBar( 2, wx.ST_SIZEGRIP, wx.ID_ANY )
		
		self.Centre( wx.BOTH )
		
		# Connect Events
		self.m_button_xbee_option.Bind( wx.EVT_BUTTON, self.on_xbee_option )
		self.m_button_toggle_xbee.Bind( wx.EVT_BUTTON, self.on_toggle_xbee )
		self.m_button_video_comm_option.Bind( wx.EVT_BUTTON, self.on_video_comm_option )
		self.m_button_toggle_video.Bind( wx.EVT_BUTTON, self.on_toggle_video )
		self.m_choice_recv_style.Bind( wx.EVT_CHOICE, self.on_recv_style_choice )
		self.m_button_recv_clear.Bind( wx.EVT_BUTTON, self.on_clear_receive )
		self.m_textCtrl_comm_send.Bind( wx.EVT_CHAR, self.on_send_area_char )
		self.m_textCtrl_comm_send.Bind( wx.EVT_TEXT_ENTER, self.on_send_area_enter )
		self.m_button_comm_send.Bind( wx.EVT_BUTTON, self.on_send_comm_click )
		self.m_button_comm_send.Bind( wx.EVT_CHAR, self.on_send_comm_char )
		self.m_radioBox_image_adj.Bind( wx.EVT_RADIOBOX, self.on_radiobox_adjust )
		self.m_slider_adjust.Bind( wx.EVT_SCROLL_CHANGED, self.on_slider_adjust_changed )
		self.m_button_track_image_show.Bind( wx.EVT_BUTTON, self.on_track_image_show )
		self.m_button_toggle_track_video.Bind( wx.EVT_BUTTON, self.on_toggle_track_video )
		self.m_button_select_object.Bind( wx.EVT_BUTTON, self.on_select_object )
		self.m_button_toggle_track.Bind( wx.EVT_BUTTON, self.on_toggle_track )
		self.m_button_video_window_show.Bind( wx.EVT_BUTTON, self.on_video_window_show )
		self.Bind( wx.EVT_MENU, self.on_save_comm_option, id = self.m_menuItem_save_comm_option.GetId() )
		self.Bind( wx.EVT_MENU, self.on_load_comm_option, id = self.m_menuItem_load_comm_option.GetId() )
		self.Bind( wx.EVT_MENU, self.on_check_comm_option, id = self.m_menuItem_check_comm_option.GetId() )
		self.Bind( wx.EVT_MENU, self.on_exit, id = self.m_menuItem_exit.GetId() )
		self.Bind( wx.EVT_MENU, self.on_about, id = self.m_menuItem_about.GetId() )
	
	def __del__( self ):
		pass
	
	
	# Virtual event handlers, overide them in your derived class
	def on_xbee_option( self, event ):
		event.Skip()
	
	def on_toggle_xbee( self, event ):
		event.Skip()
	
	def on_video_comm_option( self, event ):
		event.Skip()
	
	def on_toggle_video( self, event ):
		event.Skip()
	
	def on_recv_style_choice( self, event ):
		event.Skip()
	
	def on_clear_receive( self, event ):
		event.Skip()
	
	def on_send_area_char( self, event ):
		event.Skip()
	
	def on_send_area_enter( self, event ):
		event.Skip()
	
	def on_send_comm_click( self, event ):
		event.Skip()
	
	def on_send_comm_char( self, event ):
		event.Skip()
	
	def on_radiobox_adjust( self, event ):
		event.Skip()
	
	def on_slider_adjust_changed( self, event ):
		event.Skip()
	
	def on_track_image_show( self, event ):
		event.Skip()
	
	def on_toggle_track_video( self, event ):
		event.Skip()
	
	def on_select_object( self, event ):
		event.Skip()
	
	def on_toggle_track( self, event ):
		event.Skip()
	
	def on_video_window_show( self, event ):
		event.Skip()
	
	def on_save_comm_option( self, event ):
		event.Skip()
	
	def on_load_comm_option( self, event ):
		event.Skip()
	
	def on_check_comm_option( self, event ):
		event.Skip()
	
	def on_exit( self, event ):
		event.Skip()
	
	def on_about( self, event ):
		event.Skip()
	

###########################################################################
## Class frame_serial_setting
###########################################################################

class frame_serial_setting ( wx.Dialog ):
	
	def __init__( self, parent ):
		wx.Dialog.__init__ ( self, parent, id = wx.ID_ANY, title = u"串口设置", pos = wx.DefaultPosition, size = wx.Size( 300,400 ), style = wx.DEFAULT_DIALOG_STYLE )
		
		self.SetSizeHintsSz( wx.DefaultSize, wx.DefaultSize )
		
		bSizer3 = wx.BoxSizer( wx.VERTICAL )
		
		self.m_panel1 = wx.Panel( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
		gSizer3 = wx.GridSizer( 8, 2, 0, 0 )
		
		self.m_staticText1 = wx.StaticText( self.m_panel1, wx.ID_ANY, u"查看串口信息", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText1.Wrap( -1 )
		gSizer3.Add( self.m_staticText1, 0, wx.ALIGN_CENTER|wx.ALIGN_CENTER_HORIZONTAL|wx.ALL, 5 )
		
		self.m_button_seeComInfo = wx.Button( self.m_panel1, wx.ID_ANY, u"查看", wx.DefaultPosition, wx.DefaultSize, 0 )
		gSizer3.Add( self.m_button_seeComInfo, 0, wx.ALIGN_CENTER|wx.ALIGN_CENTER_HORIZONTAL|wx.ALL, 5 )
		
		self.m_staticText2 = wx.StaticText( self.m_panel1, wx.ID_ANY, u"选择COM口", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText2.Wrap( -1 )
		gSizer3.Add( self.m_staticText2, 0, wx.ALIGN_CENTER|wx.ALL, 5 )
		
		m_choice_comChoices = []
		self.m_choice_com = wx.Choice( self.m_panel1, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, m_choice_comChoices, 0 )
		self.m_choice_com.SetSelection( 0 )
		gSizer3.Add( self.m_choice_com, 0, wx.ALIGN_CENTER|wx.ALL, 5 )
		
		self.m_staticText3 = wx.StaticText( self.m_panel1, wx.ID_ANY, u"波特率", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText3.Wrap( -1 )
		gSizer3.Add( self.m_staticText3, 0, wx.ALIGN_CENTER|wx.ALL, 5 )
		
		m_choice_baudrateChoices = []
		self.m_choice_baudrate = wx.Choice( self.m_panel1, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, m_choice_baudrateChoices, 0 )
		self.m_choice_baudrate.SetSelection( 0 )
		gSizer3.Add( self.m_choice_baudrate, 0, wx.ALIGN_CENTER|wx.ALL, 5 )
		
		self.m_staticText4 = wx.StaticText( self.m_panel1, wx.ID_ANY, u"校验方式", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText4.Wrap( -1 )
		gSizer3.Add( self.m_staticText4, 0, wx.ALIGN_CENTER|wx.ALL, 5 )
		
		m_choice_parityChoices = []
		self.m_choice_parity = wx.Choice( self.m_panel1, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, m_choice_parityChoices, 0 )
		self.m_choice_parity.SetSelection( 0 )
		gSizer3.Add( self.m_choice_parity, 0, wx.ALIGN_CENTER|wx.ALL, 5 )
		
		self.m_staticText5 = wx.StaticText( self.m_panel1, wx.ID_ANY, u"数据位", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText5.Wrap( -1 )
		gSizer3.Add( self.m_staticText5, 0, wx.ALIGN_CENTER|wx.ALL, 5 )
		
		m_choice_bytesizeChoices = []
		self.m_choice_bytesize = wx.Choice( self.m_panel1, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, m_choice_bytesizeChoices, 0 )
		self.m_choice_bytesize.SetSelection( 0 )
		gSizer3.Add( self.m_choice_bytesize, 0, wx.ALIGN_CENTER|wx.ALL, 5 )
		
		self.m_staticText6 = wx.StaticText( self.m_panel1, wx.ID_ANY, u"停止位", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText6.Wrap( -1 )
		gSizer3.Add( self.m_staticText6, 0, wx.ALIGN_CENTER|wx.ALL, 5 )
		
		m_choice_stopbitChoices = []
		self.m_choice_stopbit = wx.Choice( self.m_panel1, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, m_choice_stopbitChoices, 0 )
		self.m_choice_stopbit.SetSelection( 0 )
		gSizer3.Add( self.m_choice_stopbit, 0, wx.ALIGN_CENTER|wx.ALL, 5 )
		
		self.m_checkBox_RtsCts = wx.CheckBox( self.m_panel1, wx.ID_ANY, u"RtsCts", wx.DefaultPosition, wx.DefaultSize, 0 )
		gSizer3.Add( self.m_checkBox_RtsCts, 0, wx.ALIGN_CENTER|wx.ALL, 5 )
		
		self.m_checkBox_XonXoff = wx.CheckBox( self.m_panel1, wx.ID_ANY, u"XonXoff", wx.DefaultPosition, wx.DefaultSize, 0 )
		gSizer3.Add( self.m_checkBox_XonXoff, 0, wx.ALIGN_CENTER|wx.ALL, 5 )
		
		self.m_button_ok = wx.Button( self.m_panel1, wx.ID_OK, u"确认", wx.DefaultPosition, wx.DefaultSize, 0 )
		gSizer3.Add( self.m_button_ok, 0, wx.ALIGN_CENTER|wx.ALL, 5 )
		
		self.m_button_cancel = wx.Button( self.m_panel1, wx.ID_CANCEL, u"取消", wx.DefaultPosition, wx.DefaultSize, 0 )
		gSizer3.Add( self.m_button_cancel, 0, wx.ALIGN_CENTER|wx.ALL, 5 )
		
		self.m_panel1.SetSizer( gSizer3 )
		self.m_panel1.Layout()
		gSizer3.Fit( self.m_panel1 )
		bSizer3.Add( self.m_panel1, 1, wx.EXPAND |wx.ALL, 0 )
		
		self.SetSizer( bSizer3 )
		self.Layout()
		
		self.Centre( wx.BOTH )
		
		# Connect Events
		self.m_button_seeComInfo.Bind( wx.EVT_BUTTON, self.on_see_com_info )
	
	def __del__( self ):
		pass
	
	
	# Virtual event handlers, overide them in your derived class
	def on_see_com_info( self, event ):
		event.Skip()
	

