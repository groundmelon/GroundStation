# -*- coding: utf-8 -*- 

###########################################################################
## Python code generated with wxFormBuilder (version Feb 26 2014)
## http://www.wxformbuilder.org/
##
## PLEASE DO "NOT" EDIT THIS FILE!
###########################################################################

import wx
import wx.xrc
import wx.grid

###########################################################################
## Class FrameGroundStationBase
###########################################################################

class FrameGroundStationBase ( wx.Frame ):
	
	def __init__( self, parent ):
		wx.Frame.__init__ ( self, parent, id = wx.ID_ANY, title = u"GroundStation", pos = wx.DefaultPosition, size = wx.Size( 700,600 ), style = wx.DEFAULT_FRAME_STYLE|wx.CLIP_CHILDREN|wx.TAB_TRAVERSAL )
		
		self.SetSizeHintsSz( wx.Size( -1,-1 ), wx.DefaultSize )
		
		bSizer2 = wx.BoxSizer( wx.VERTICAL )
		
		self.m_panel2 = wx.Panel( self, wx.ID_ANY, wx.DefaultPosition, wx.Size( -1,-1 ), wx.TAB_TRAVERSAL )
		self.m_panel2.SetForegroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_WINDOWTEXT ) )
		self.m_panel2.SetBackgroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_MENU ) )
		
		gbSizer1 = wx.GridBagSizer( 0, 0 )
		gbSizer1.SetFlexibleDirection( wx.BOTH )
		gbSizer1.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_SPECIFIED )
		
		gSizer2 = wx.GridSizer( 3, 2, 0, 0 )
		
		self.m_button_xbee_option = wx.Button( self.m_panel2, wx.ID_ANY, u"XBee通信设置", wx.DefaultPosition, wx.Size( -1,-1 ), 0 )
		gSizer2.Add( self.m_button_xbee_option, 0, wx.ALIGN_CENTER|wx.ALL, 5 )
		
		self.m_button_video_comm_option = wx.Button( self.m_panel2, wx.ID_ANY, u"图传通信设置", wx.DefaultPosition, wx.Size( -1,-1 ), 0 )
		gSizer2.Add( self.m_button_video_comm_option, 0, wx.ALIGN_CENTER|wx.ALL, 5 )
		
		self.m_button_toggle_xbee = wx.Button( self.m_panel2, wx.ID_ANY, u"开始Xbee通信", wx.DefaultPosition, wx.Size( -1,-1 ), 0 )
		gSizer2.Add( self.m_button_toggle_xbee, 0, wx.ALIGN_CENTER|wx.ALL, 5 )
		
		self.m_button_toggle_video = wx.Button( self.m_panel2, wx.ID_ANY, u"开始图像传输", wx.DefaultPosition, wx.Size( -1,-1 ), 0 )
		gSizer2.Add( self.m_button_toggle_video, 0, wx.ALIGN_CENTER|wx.ALL, 5 )
		
		self.m_button_update_uavinfo = wx.Button( self.m_panel2, wx.ID_ANY, u"更新UAV状态", wx.DefaultPosition, wx.DefaultSize, 0 )
		gSizer2.Add( self.m_button_update_uavinfo, 0, wx.ALL, 5 )
		
		
		gbSizer1.Add( gSizer2, wx.GBPosition( 0, 0 ), wx.GBSpan( 1, 2 ), wx.ALIGN_LEFT|wx.ALIGN_TOP, 5 )
		
		self.m_bitmap_attitude = wx.StaticBitmap( self.m_panel2, wx.ID_ANY, wx.NullBitmap, wx.DefaultPosition, wx.Size( 100,100 ), 0 )
		gbSizer1.Add( self.m_bitmap_attitude, wx.GBPosition( 0, 2 ), wx.GBSpan( 1, 1 ), wx.ALIGN_CENTER, 5 )
		
		gSizer4 = wx.GridSizer( 5, 2, 0, 0 )
		
		self.m_staticText11 = wx.StaticText( self.m_panel2, wx.ID_ANY, u"高度", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText11.Wrap( -1 )
		gSizer4.Add( self.m_staticText11, 0, wx.ALIGN_RIGHT|wx.ALL, 5 )
		
		self.m_staticText_height = wx.StaticText( self.m_panel2, wx.ID_ANY, u"000.00m", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText_height.Wrap( -1 )
		self.m_staticText_height.SetFont( wx.Font( wx.NORMAL_FONT.GetPointSize(), 70, 90, 90, False, "Consolas" ) )
		
		gSizer4.Add( self.m_staticText_height, 0, wx.ALIGN_CENTER_VERTICAL|wx.ALIGN_LEFT|wx.ALL, 5 )
		
		self.m_staticText12 = wx.StaticText( self.m_panel2, wx.ID_ANY, u"电压", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText12.Wrap( -1 )
		gSizer4.Add( self.m_staticText12, 0, wx.ALIGN_RIGHT|wx.ALL, 5 )
		
		self.m_staticText_vol = wx.StaticText( self.m_panel2, wx.ID_ANY, u"00.000v", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText_vol.Wrap( -1 )
		self.m_staticText_vol.SetFont( wx.Font( wx.NORMAL_FONT.GetPointSize(), 70, 90, 90, False, "Consolas" ) )
		
		gSizer4.Add( self.m_staticText_vol, 0, wx.ALIGN_CENTER_VERTICAL|wx.ALIGN_LEFT|wx.ALL, 5 )
		
		self.m_staticText15 = wx.StaticText( self.m_panel2, wx.ID_ANY, u"俯仰", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText15.Wrap( -1 )
		gSizer4.Add( self.m_staticText15, 0, wx.ALIGN_RIGHT|wx.ALL, 5 )
		
		self.m_staticText_pitch = wx.StaticText( self.m_panel2, wx.ID_ANY, u"0.0000d", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText_pitch.Wrap( -1 )
		self.m_staticText_pitch.SetFont( wx.Font( wx.NORMAL_FONT.GetPointSize(), 70, 90, 90, False, "Consolas" ) )
		
		gSizer4.Add( self.m_staticText_pitch, 0, wx.ALIGN_LEFT|wx.ALL, 5 )
		
		self.m_staticText17 = wx.StaticText( self.m_panel2, wx.ID_ANY, u"横滚", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText17.Wrap( -1 )
		gSizer4.Add( self.m_staticText17, 0, wx.ALIGN_RIGHT|wx.ALL, 5 )
		
		self.m_staticText_roll = wx.StaticText( self.m_panel2, wx.ID_ANY, u"0.0000d", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText_roll.Wrap( -1 )
		self.m_staticText_roll.SetFont( wx.Font( wx.NORMAL_FONT.GetPointSize(), 70, 90, 90, False, "Consolas" ) )
		
		gSizer4.Add( self.m_staticText_roll, 0, wx.ALIGN_LEFT|wx.ALL, 5 )
		
		self.m_staticText19 = wx.StaticText( self.m_panel2, wx.ID_ANY, u"偏航", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText19.Wrap( -1 )
		gSizer4.Add( self.m_staticText19, 0, wx.ALIGN_RIGHT|wx.ALL, 5 )
		
		self.m_staticText_yaw = wx.StaticText( self.m_panel2, wx.ID_ANY, u"0.0000d", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText_yaw.Wrap( -1 )
		self.m_staticText_yaw.SetFont( wx.Font( wx.NORMAL_FONT.GetPointSize(), 70, 90, 90, False, "Consolas" ) )
		
		gSizer4.Add( self.m_staticText_yaw, 0, wx.ALIGN_LEFT|wx.ALL, 5 )
		
		
		gbSizer1.Add( gSizer4, wx.GBPosition( 0, 3 ), wx.GBSpan( 1, 1 ), wx.ALIGN_CENTER, 5 )
		
		self.m_notebook1 = wx.Notebook( self.m_panel2, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_panel_comm = wx.Panel( self.m_notebook1, wx.ID_ANY, wx.DefaultPosition, wx.Size( -1,-1 ), wx.TAB_TRAVERSAL )
		self.m_panel_comm.SetBackgroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_BTNFACE ) )
		
		gbSizer6 = wx.GridBagSizer( 0, 0 )
		gbSizer6.SetFlexibleDirection( wx.BOTH )
		gbSizer6.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_SPECIFIED )
		
		self.m_staticText7 = wx.StaticText( self.m_panel_comm, wx.ID_ANY, u"接收区", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText7.Wrap( -1 )
		gbSizer6.Add( self.m_staticText7, wx.GBPosition( 0, 0 ), wx.GBSpan( 1, 1 ), wx.ALL, 5 )
		
		self.m_textCtrl_comm_receive = wx.TextCtrl( self.m_panel_comm, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, wx.TE_MULTILINE|wx.TE_WORDWRAP )
		self.m_textCtrl_comm_receive.SetMaxLength( 0 ) 
		self.m_textCtrl_comm_receive.SetFont( wx.Font( wx.NORMAL_FONT.GetPointSize(), 70, 90, 90, False, "Consolas" ) )
		self.m_textCtrl_comm_receive.SetMinSize( wx.Size( -1,160 ) )
		
		gbSizer6.Add( self.m_textCtrl_comm_receive, wx.GBPosition( 1, 0 ), wx.GBSpan( 1, 4 ), wx.ALL|wx.EXPAND, 5 )
		
		m_choice_recv_styleChoices = [ u"ASCII", u"HEX" ]
		self.m_choice_recv_style = wx.Choice( self.m_panel_comm, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, m_choice_recv_styleChoices, 0 )
		self.m_choice_recv_style.SetSelection( 1 )
		gbSizer6.Add( self.m_choice_recv_style, wx.GBPosition( 2, 2 ), wx.GBSpan( 1, 1 ), wx.ALIGN_CENTER|wx.ALL, 5 )
		
		self.m_button_recv_clear = wx.Button( self.m_panel_comm, wx.ID_ANY, u"清除接收缓冲区", wx.DefaultPosition, wx.DefaultSize, 0 )
		gbSizer6.Add( self.m_button_recv_clear, wx.GBPosition( 2, 3 ), wx.GBSpan( 1, 1 ), wx.ALIGN_CENTER|wx.ALL, 5 )
		
		self.m_staticText8 = wx.StaticText( self.m_panel_comm, wx.ID_ANY, u"发送区", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText8.Wrap( -1 )
		gbSizer6.Add( self.m_staticText8, wx.GBPosition( 3, 0 ), wx.GBSpan( 1, 1 ), wx.ALL, 5 )
		
		self.m_textCtrl_comm_send = wx.TextCtrl( self.m_panel_comm, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.Size( -1,-1 ), wx.TE_PROCESS_ENTER )
		self.m_textCtrl_comm_send.SetMaxLength( 0 ) 
		self.m_textCtrl_comm_send.SetFont( wx.Font( wx.NORMAL_FONT.GetPointSize(), 70, 90, 90, False, "Consolas" ) )
		
		gbSizer6.Add( self.m_textCtrl_comm_send, wx.GBPosition( 4, 0 ), wx.GBSpan( 1, 4 ), wx.ALL|wx.EXPAND, 5 )
		
		m_choice_send_styleChoices = [ u"ASCII", u"HEX" ]
		self.m_choice_send_style = wx.Choice( self.m_panel_comm, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, m_choice_send_styleChoices, 0 )
		self.m_choice_send_style.SetSelection( 1 )
		gbSizer6.Add( self.m_choice_send_style, wx.GBPosition( 5, 2 ), wx.GBSpan( 1, 1 ), wx.ALIGN_CENTER|wx.ALL, 5 )
		
		self.m_button_comm_send = wx.Button( self.m_panel_comm, wx.ID_ANY, u"发送指令", wx.DefaultPosition, wx.DefaultSize, 0 )
		gbSizer6.Add( self.m_button_comm_send, wx.GBPosition( 5, 3 ), wx.GBSpan( 1, 1 ), wx.ALIGN_CENTER|wx.ALL|wx.EXPAND, 5 )
		
		self.m_checkBox_sent_clear = wx.CheckBox( self.m_panel_comm, wx.ID_ANY, u"发送后清空", wx.DefaultPosition, wx.DefaultSize, 0 )
		gbSizer6.Add( self.m_checkBox_sent_clear, wx.GBPosition( 5, 1 ), wx.GBSpan( 1, 1 ), wx.ALIGN_CENTER|wx.ALL|wx.EXPAND, 5 )
		
		
		self.m_panel_comm.SetSizer( gbSizer6 )
		self.m_panel_comm.Layout()
		gbSizer6.Fit( self.m_panel_comm )
		self.m_notebook1.AddPage( self.m_panel_comm, u"通信数据查看", True )
		self.m_panel_para_adj = wx.Panel( self.m_notebook1, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
		gbSizer11 = wx.GridBagSizer( 0, 0 )
		gbSizer11.SetFlexibleDirection( wx.BOTH )
		gbSizer11.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_SPECIFIED )
		
		self.m_grid_para_adj = wx.grid.Grid( self.m_panel_para_adj, wx.ID_ANY, wx.DefaultPosition, wx.Size( -1,-1 ), 0 )
		
		# Grid
		self.m_grid_para_adj.CreateGrid( 9, 1 )
		self.m_grid_para_adj.EnableEditing( True )
		self.m_grid_para_adj.EnableGridLines( True )
		self.m_grid_para_adj.EnableDragGridSize( False )
		self.m_grid_para_adj.SetMargins( 0, 0 )
		
		# Columns
		self.m_grid_para_adj.EnableDragColMove( False )
		self.m_grid_para_adj.EnableDragColSize( True )
		self.m_grid_para_adj.SetColLabelSize( 30 )
		self.m_grid_para_adj.SetColLabelValue( 0, u"Value" )
		self.m_grid_para_adj.SetColLabelAlignment( wx.ALIGN_CENTRE, wx.ALIGN_CENTRE )
		
		# Rows
		self.m_grid_para_adj.EnableDragRowSize( True )
		self.m_grid_para_adj.SetRowLabelSize( 60 )
		self.m_grid_para_adj.SetRowLabelValue( 0, u"XP" )
		self.m_grid_para_adj.SetRowLabelValue( 1, u"XI" )
		self.m_grid_para_adj.SetRowLabelValue( 2, u"XD" )
		self.m_grid_para_adj.SetRowLabelValue( 3, u"YP" )
		self.m_grid_para_adj.SetRowLabelValue( 4, u"YI" )
		self.m_grid_para_adj.SetRowLabelValue( 5, u"YD" )
		self.m_grid_para_adj.SetRowLabelValue( 6, u"ZP" )
		self.m_grid_para_adj.SetRowLabelValue( 7, u"ZI" )
		self.m_grid_para_adj.SetRowLabelValue( 8, u"ZD" )
		self.m_grid_para_adj.SetRowLabelAlignment( wx.ALIGN_CENTRE, wx.ALIGN_CENTRE )
		
		# Label Appearance
		
		# Cell Defaults
		self.m_grid_para_adj.SetDefaultCellAlignment( wx.ALIGN_CENTRE, wx.ALIGN_CENTRE )
		gbSizer11.Add( self.m_grid_para_adj, wx.GBPosition( 0, 0 ), wx.GBSpan( 1, 2 ), wx.ALIGN_CENTER|wx.ALL, 5 )
		
		self.m_button_send_para = wx.Button( self.m_panel_para_adj, wx.ID_ANY, u"发送参数", wx.DefaultPosition, wx.DefaultSize, 0 )
		gbSizer11.Add( self.m_button_send_para, wx.GBPosition( 1, 0 ), wx.GBSpan( 1, 1 ), wx.ALL, 5 )
		
		self.m_button_set_down_para = wx.Button( self.m_panel_para_adj, wx.ID_ANY, u"固定参数", wx.DefaultPosition, wx.DefaultSize, 0 )
		gbSizer11.Add( self.m_button_set_down_para, wx.GBPosition( 1, 1 ), wx.GBSpan( 1, 1 ), wx.ALL, 5 )
		
		self.m_button_save_para = wx.Button( self.m_panel_para_adj, wx.ID_ANY, u"保存参数", wx.DefaultPosition, wx.DefaultSize, 0 )
		gbSizer11.Add( self.m_button_save_para, wx.GBPosition( 2, 0 ), wx.GBSpan( 1, 1 ), wx.ALL, 5 )
		
		self.m_button_load_para = wx.Button( self.m_panel_para_adj, wx.ID_ANY, u"读取参数", wx.DefaultPosition, wx.DefaultSize, 0 )
		gbSizer11.Add( self.m_button_load_para, wx.GBPosition( 2, 1 ), wx.GBSpan( 1, 1 ), wx.ALL, 5 )
		
		self.m_textCtrl_showpid = wx.TextCtrl( self.m_panel_para_adj, wx.ID_ANY, u"机上PID参数", wx.DefaultPosition, wx.Size( 120,200 ), wx.TE_CENTRE|wx.TE_MULTILINE|wx.TE_NO_VSCROLL|wx.TE_READONLY )
		self.m_textCtrl_showpid.SetFont( wx.Font( wx.NORMAL_FONT.GetPointSize(), 70, 90, 90, False, "Consolas" ) )
		
		gbSizer11.Add( self.m_textCtrl_showpid, wx.GBPosition( 0, 2 ), wx.GBSpan( 1, 1 ), wx.ALL, 5 )
		
		
		self.m_panel_para_adj.SetSizer( gbSizer11 )
		self.m_panel_para_adj.Layout()
		gbSizer11.Fit( self.m_panel_para_adj )
		self.m_notebook1.AddPage( self.m_panel_para_adj, u"调参", False )
		self.m_panel_track = wx.Panel( self.m_notebook1, wx.ID_ANY, wx.DefaultPosition, wx.Size( -1,-1 ), wx.TAB_TRAVERSAL )
		self.m_panel_track.SetBackgroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_BTNFACE ) )
		self.m_panel_track.Enable( False )
		
		gbSizer3 = wx.GridBagSizer( 0, 0 )
		gbSizer3.SetFlexibleDirection( wx.BOTH )
		gbSizer3.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_SPECIFIED )
		
		self.m_bitmap_track = wx.StaticBitmap( self.m_panel_track, wx.ID_ANY, wx.Bitmap( u"resources/null.bmp", wx.BITMAP_TYPE_ANY ), wx.DefaultPosition, wx.Size( 320,240 ), 0 )
		self.m_menu_bitmap_track = wx.Menu()
		self.m_menuItem_track_display_rst = wx.MenuItem( self.m_menu_bitmap_track, wx.ID_ANY, u"显示结果", wx.EmptyString, wx.ITEM_RADIO )
		self.m_menu_bitmap_track.AppendItem( self.m_menuItem_track_display_rst )
		
		self.m_menuItem_track_display_process = wx.MenuItem( self.m_menu_bitmap_track, wx.ID_ANY, u"显示过程", wx.EmptyString, wx.ITEM_RADIO )
		self.m_menu_bitmap_track.AppendItem( self.m_menuItem_track_display_process )
		
		self.m_menu_bitmap_track.AppendSeparator()
		
		self.m_menuItem_track_hist_h = wx.MenuItem( self.m_menu_bitmap_track, wx.ID_ANY, u"色调基准（色彩）", wx.EmptyString, wx.ITEM_RADIO )
		self.m_menu_bitmap_track.AppendItem( self.m_menuItem_track_hist_h )
		
		self.m_menuItem_track_hist_s = wx.MenuItem( self.m_menu_bitmap_track, wx.ID_ANY, u"饱和基准（灰度）", wx.EmptyString, wx.ITEM_RADIO )
		self.m_menu_bitmap_track.AppendItem( self.m_menuItem_track_hist_s )
		
		self.m_menuItem_track_hist_l = wx.MenuItem( self.m_menu_bitmap_track, wx.ID_ANY, u"亮度基准（亮暗）", wx.EmptyString, wx.ITEM_RADIO )
		self.m_menu_bitmap_track.AppendItem( self.m_menuItem_track_hist_l )
		
		self.m_bitmap_track.Bind( wx.EVT_RIGHT_DOWN, self.m_bitmap_trackOnContextMenu ) 
		
		gbSizer3.Add( self.m_bitmap_track, wx.GBPosition( 0, 0 ), wx.GBSpan( 1, 4 ), wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_TOP|wx.ALL, 5 )
		
		m_radioBox_image_adjChoices = [ u"Brightness", u"Contrast", u"Gamma" ]
		self.m_radioBox_image_adj = wx.RadioBox( self.m_panel_track, wx.ID_ANY, u"Adjust", wx.DefaultPosition, wx.DefaultSize, m_radioBox_image_adjChoices, 1, wx.RA_SPECIFY_COLS )
		self.m_radioBox_image_adj.SetSelection( 0 )
		gbSizer3.Add( self.m_radioBox_image_adj, wx.GBPosition( 1, 0 ), wx.GBSpan( 1, 1 ), wx.ALL, 1 )
		
		gbSizer4 = wx.GridBagSizer( 0, 0 )
		gbSizer4.SetFlexibleDirection( wx.BOTH )
		gbSizer4.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_SPECIFIED )
		
		self.m_staticText_adjust_type = wx.StaticText( self.m_panel_track, wx.ID_ANY, u"Brightness", wx.DefaultPosition, wx.Size( 60,-1 ), 0 )
		self.m_staticText_adjust_type.Wrap( -1 )
		gbSizer4.Add( self.m_staticText_adjust_type, wx.GBPosition( 0, 0 ), wx.GBSpan( 1, 1 ), wx.ALIGN_CENTER|wx.ALL, 5 )
		
		self.m_slider_adjust = wx.Slider( self.m_panel_track, wx.ID_ANY, 50, 0, 100, wx.DefaultPosition, wx.Size( -1,-1 ), wx.SL_HORIZONTAL )
		gbSizer4.Add( self.m_slider_adjust, wx.GBPosition( 0, 1 ), wx.GBSpan( 1, 2 ), wx.ALIGN_CENTER|wx.EXPAND, 1 )
		
		self.m_button_toggle_track_video = wx.Button( self.m_panel_track, wx.ID_ANY, u"显示视频", wx.DefaultPosition, wx.Size( 80,-1 ), 0 )
		gbSizer4.Add( self.m_button_toggle_track_video, wx.GBPosition( 1, 0 ), wx.GBSpan( 1, 1 ), wx.ALL, 1 )
		
		self.m_button_select_object = wx.Button( self.m_panel_track, wx.ID_ANY, u"框选目标", wx.DefaultPosition, wx.Size( 80,-1 ), 0 )
		gbSizer4.Add( self.m_button_select_object, wx.GBPosition( 1, 1 ), wx.GBSpan( 1, 1 ), wx.ALL, 1 )
		
		self.m_button_toggle_track = wx.Button( self.m_panel_track, wx.ID_ANY, u"开始追踪", wx.DefaultPosition, wx.Size( 80,-1 ), 0 )
		gbSizer4.Add( self.m_button_toggle_track, wx.GBPosition( 1, 2 ), wx.GBSpan( 1, 1 ), wx.ALL, 1 )
		
		m_choice_track_modeChoices = [ u"template", u"edge-tpl", u"meanshift", u"multi-meanshift", u"color", u"mix" ]
		self.m_choice_track_mode = wx.Choice( self.m_panel_track, wx.ID_ANY, wx.DefaultPosition, wx.Size( -1,-1 ), m_choice_track_modeChoices, 0 )
		self.m_choice_track_mode.SetSelection( 0 )
		self.m_choice_track_mode.SetMaxSize( wx.Size( 80,-1 ) )
		
		gbSizer4.Add( self.m_choice_track_mode, wx.GBPosition( 2, 0 ), wx.GBSpan( 1, 1 ), wx.ALL, 1 )
		
		m_choice_track_argChoices = [ u"multi", u"edge" ]
		self.m_choice_track_arg = wx.Choice( self.m_panel_track, wx.ID_ANY, wx.DefaultPosition, wx.Size( -1,-1 ), m_choice_track_argChoices, 0 )
		self.m_choice_track_arg.SetSelection( 0 )
		gbSizer4.Add( self.m_choice_track_arg, wx.GBPosition( 2, 1 ), wx.GBSpan( 1, 1 ), wx.ALIGN_CENTER, 5 )
		
		self.m_textCtrl_track_arg = wx.TextCtrl( self.m_panel_track, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, wx.TE_PROCESS_ENTER )
		self.m_textCtrl_track_arg.SetMaxSize( wx.Size( 80,-1 ) )
		
		gbSizer4.Add( self.m_textCtrl_track_arg, wx.GBPosition( 2, 2 ), wx.GBSpan( 1, 1 ), wx.ALIGN_CENTER, 5 )
		
		
		gbSizer3.Add( gbSizer4, wx.GBPosition( 1, 1 ), wx.GBSpan( 1, 3 ), wx.EXPAND, 0 )
		
		
		self.m_panel_track.SetSizer( gbSizer3 )
		self.m_panel_track.Layout()
		gbSizer3.Fit( self.m_panel_track )
		self.m_notebook1.AddPage( self.m_panel_track, u"目标跟踪", False )
		self.m_panel_route = wx.Panel( self.m_notebook1, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
		self.m_panel_route.SetBackgroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_BTNFACE ) )
		
		bSizer_ge = wx.BoxSizer( wx.VERTICAL )
		
		
		self.m_panel_route.SetSizer( bSizer_ge )
		self.m_panel_route.Layout()
		bSizer_ge.Fit( self.m_panel_route )
		self.m_notebook1.AddPage( self.m_panel_route, u"路径规划", False )
		
		gbSizer1.Add( self.m_notebook1, wx.GBPosition( 1, 0 ), wx.GBSpan( 1, 2 ), wx.ALIGN_LEFT|wx.ALIGN_TOP|wx.ALL|wx.EXPAND, 0 )
		
		self.m_notebook2 = wx.Notebook( self.m_panel2, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_notebook2.SetBackgroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_BTNFACE ) )
		
		self.m_panel_image = wx.Panel( self.m_notebook2, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
		self.m_panel_image.SetBackgroundColour( wx.Colour( 240, 240, 240 ) )
		
		gbSizer5 = wx.GridBagSizer( 0, 0 )
		gbSizer5.SetFlexibleDirection( wx.BOTH )
		gbSizer5.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_NONE )
		
		self.m_bitmap_video = wx.StaticBitmap( self.m_panel_image, wx.ID_ANY, wx.Bitmap( u"resources/null.bmp", wx.BITMAP_TYPE_ANY ), wx.DefaultPosition, wx.Size( 320,240 ), wx.CLIP_CHILDREN )
		self.m_menu_bitmap_video = wx.Menu()
		self.m_menuItem_video_osd = wx.MenuItem( self.m_menu_bitmap_video, wx.ID_ANY, u"OSD", wx.EmptyString, wx.ITEM_CHECK )
		self.m_menu_bitmap_video.AppendItem( self.m_menuItem_video_osd )
		self.m_menuItem_video_osd.Check( True )
		
		self.m_menu_bitmap_video.AppendSeparator()
		
		self.m_bitmap_video.Bind( wx.EVT_RIGHT_DOWN, self.m_bitmap_videoOnContextMenu ) 
		
		gbSizer5.Add( self.m_bitmap_video, wx.GBPosition( 0, 0 ), wx.GBSpan( 1, 4 ), wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_TOP|wx.ALL, 5 )
		
		self.m_button_video_window_show = wx.Button( self.m_panel_image, wx.ID_ANY, u"独立窗口", wx.DefaultPosition, wx.DefaultSize, 0 )
		gbSizer5.Add( self.m_button_video_window_show, wx.GBPosition( 1, 1 ), wx.GBSpan( 1, 1 ), wx.ALIGN_CENTER|wx.ALL, 5 )
		
		self.m_button_record = wx.Button( self.m_panel_image, wx.ID_ANY, u"开始录像", wx.DefaultPosition, wx.DefaultSize, 0 )
		gbSizer5.Add( self.m_button_record, wx.GBPosition( 1, 2 ), wx.GBSpan( 1, 1 ), wx.ALL, 5 )
		
		self.m_filePicker_output = wx.FilePickerCtrl( self.m_panel_image, wx.ID_ANY, u"_Output.avi", u"输出录像到", u"*.avi", wx.DefaultPosition, wx.DefaultSize, wx.FLP_SAVE|wx.FLP_USE_TEXTCTRL )
		gbSizer5.Add( self.m_filePicker_output, wx.GBPosition( 2, 0 ), wx.GBSpan( 1, 4 ), wx.ALL|wx.EXPAND, 5 )
		
		
		self.m_panel_image.SetSizer( gbSizer5 )
		self.m_panel_image.Layout()
		gbSizer5.Fit( self.m_panel_image )
		self.m_notebook2.AddPage( self.m_panel_image, u"实时图像", False )
		
		gbSizer1.Add( self.m_notebook2, wx.GBPosition( 1, 2 ), wx.GBSpan( 1, 2 ), wx.ALIGN_LEFT|wx.ALIGN_TOP|wx.EXPAND, 0 )
		
		
		self.m_panel2.SetSizer( gbSizer1 )
		self.m_panel2.Layout()
		gbSizer1.Fit( self.m_panel2 )
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
		self.m_button_video_comm_option.Bind( wx.EVT_BUTTON, self.on_video_comm_option )
		self.m_button_toggle_xbee.Bind( wx.EVT_BUTTON, self.on_toggle_xbee )
		self.m_button_toggle_video.Bind( wx.EVT_BUTTON, self.on_toggle_video )
		self.m_button_update_uavinfo.Bind( wx.EVT_BUTTON, self.on_update_uavinfo )
		self.m_choice_recv_style.Bind( wx.EVT_CHOICE, self.on_recv_style_choice )
		self.m_button_recv_clear.Bind( wx.EVT_BUTTON, self.on_clear_receive )
		self.m_textCtrl_comm_send.Bind( wx.EVT_CHAR, self.on_send_area_char )
		self.m_textCtrl_comm_send.Bind( wx.EVT_TEXT_ENTER, self.on_send_area_enter )
		self.m_button_comm_send.Bind( wx.EVT_BUTTON, self.on_send_comm_click )
		self.m_button_comm_send.Bind( wx.EVT_CHAR, self.on_send_comm_char )
		self.m_button_send_para.Bind( wx.EVT_BUTTON, self.on_send_para )
		self.m_button_set_down_para.Bind( wx.EVT_BUTTON, self.on_set_down_para )
		self.m_button_save_para.Bind( wx.EVT_BUTTON, self.on_save_para )
		self.m_button_load_para.Bind( wx.EVT_BUTTON, self.on_load_para )
		self.m_bitmap_track.Bind( wx.EVT_ENTER_WINDOW, self.on_enter_bitmap_track )
		self.m_bitmap_track.Bind( wx.EVT_LEAVE_WINDOW, self.on_leave_bitmap_track )
		self.m_radioBox_image_adj.Bind( wx.EVT_RADIOBOX, self.on_radiobox_adjust )
		self.m_slider_adjust.Bind( wx.EVT_SCROLL_CHANGED, self.on_slider_adjust_changed )
		self.m_button_toggle_track_video.Bind( wx.EVT_BUTTON, self.on_toggle_track_video )
		self.m_button_select_object.Bind( wx.EVT_BUTTON, self.on_select_object )
		self.m_button_toggle_track.Bind( wx.EVT_BUTTON, self.on_toggle_track )
		self.m_textCtrl_track_arg.Bind( wx.EVT_TEXT_ENTER, self.on_track_arg_enter )
		self.m_bitmap_video.Bind( wx.EVT_ENTER_WINDOW, self.on_enter_bitmap_video )
		self.m_bitmap_video.Bind( wx.EVT_LEAVE_WINDOW, self.on_leave_bitmap_video )
		self.m_button_video_window_show.Bind( wx.EVT_BUTTON, self.on_video_window_show )
		self.m_button_record.Bind( wx.EVT_BUTTON, self.on_record )
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
	
	def on_video_comm_option( self, event ):
		event.Skip()
	
	def on_toggle_xbee( self, event ):
		event.Skip()
	
	def on_toggle_video( self, event ):
		event.Skip()
	
	def on_update_uavinfo( self, event ):
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
	
	def on_send_para( self, event ):
		event.Skip()
	
	def on_set_down_para( self, event ):
		event.Skip()
	
	def on_save_para( self, event ):
		event.Skip()
	
	def on_load_para( self, event ):
		event.Skip()
	
	def on_enter_bitmap_track( self, event ):
		event.Skip()
	
	def on_leave_bitmap_track( self, event ):
		event.Skip()
	
	def on_radiobox_adjust( self, event ):
		event.Skip()
	
	def on_slider_adjust_changed( self, event ):
		event.Skip()
	
	def on_toggle_track_video( self, event ):
		event.Skip()
	
	def on_select_object( self, event ):
		event.Skip()
	
	def on_toggle_track( self, event ):
		event.Skip()
	
	def on_track_arg_enter( self, event ):
		event.Skip()
	
	def on_enter_bitmap_video( self, event ):
		event.Skip()
	
	def on_leave_bitmap_video( self, event ):
		event.Skip()
	
	def on_video_window_show( self, event ):
		event.Skip()
	
	def on_record( self, event ):
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
	
	def m_bitmap_trackOnContextMenu( self, event ):
		self.m_bitmap_track.PopupMenu( self.m_menu_bitmap_track, event.GetPosition() )
		
	def m_bitmap_videoOnContextMenu( self, event ):
		self.m_bitmap_video.PopupMenu( self.m_menu_bitmap_video, event.GetPosition() )
		

###########################################################################
## Class frame_serial_setting
###########################################################################

class frame_serial_setting ( wx.Dialog ):
	
	def __init__( self, parent ):
		wx.Dialog.__init__ ( self, parent, id = wx.ID_ANY, title = u"串口设置", pos = wx.DefaultPosition, size = wx.Size( 300,320 ), style = wx.DEFAULT_DIALOG_STYLE )
		
		self.SetSizeHintsSz( wx.DefaultSize, wx.DefaultSize )
		
		bSizer3 = wx.BoxSizer( wx.VERTICAL )
		
		self.m_panel1 = wx.Panel( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
		gSizer3 = wx.GridSizer( 8, 2, 0, 0 )
		
		self.m_staticText1 = wx.StaticText( self.m_panel1, wx.ID_ANY, u"查看串口信息", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText1.Wrap( -1 )
		gSizer3.Add( self.m_staticText1, 0, wx.ALIGN_CENTER|wx.ALIGN_CENTER_HORIZONTAL|wx.ALL, 5 )
		
		self.m_button_seeComInfo = wx.Button( self.m_panel1, wx.ID_ANY, u"查看", wx.DefaultPosition, wx.Size( 100,-1 ), 0 )
		gSizer3.Add( self.m_button_seeComInfo, 0, wx.ALIGN_CENTER|wx.ALIGN_CENTER_HORIZONTAL|wx.ALL, 5 )
		
		self.m_staticText2 = wx.StaticText( self.m_panel1, wx.ID_ANY, u"选择COM口", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText2.Wrap( -1 )
		gSizer3.Add( self.m_staticText2, 0, wx.ALIGN_CENTER|wx.ALL, 5 )
		
		m_choice_comChoices = []
		self.m_choice_com = wx.Choice( self.m_panel1, wx.ID_ANY, wx.DefaultPosition, wx.Size( 100,-1 ), m_choice_comChoices, 0 )
		self.m_choice_com.SetSelection( 0 )
		gSizer3.Add( self.m_choice_com, 0, wx.ALIGN_CENTER|wx.ALL, 5 )
		
		self.m_staticText3 = wx.StaticText( self.m_panel1, wx.ID_ANY, u"波特率", wx.DefaultPosition, wx.Size( -1,-1 ), 0 )
		self.m_staticText3.Wrap( -1 )
		gSizer3.Add( self.m_staticText3, 0, wx.ALIGN_CENTER|wx.ALL, 5 )
		
		m_choice_baudrateChoices = []
		self.m_choice_baudrate = wx.Choice( self.m_panel1, wx.ID_ANY, wx.DefaultPosition, wx.Size( 100,-1 ), m_choice_baudrateChoices, 0 )
		self.m_choice_baudrate.SetSelection( 0 )
		gSizer3.Add( self.m_choice_baudrate, 0, wx.ALIGN_CENTER|wx.ALL, 5 )
		
		self.m_staticText4 = wx.StaticText( self.m_panel1, wx.ID_ANY, u"校验方式", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText4.Wrap( -1 )
		gSizer3.Add( self.m_staticText4, 0, wx.ALIGN_CENTER|wx.ALL, 5 )
		
		m_choice_parityChoices = []
		self.m_choice_parity = wx.Choice( self.m_panel1, wx.ID_ANY, wx.DefaultPosition, wx.Size( 100,-1 ), m_choice_parityChoices, 0 )
		self.m_choice_parity.SetSelection( 0 )
		gSizer3.Add( self.m_choice_parity, 0, wx.ALIGN_CENTER|wx.ALL, 5 )
		
		self.m_staticText5 = wx.StaticText( self.m_panel1, wx.ID_ANY, u"数据位", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText5.Wrap( -1 )
		gSizer3.Add( self.m_staticText5, 0, wx.ALIGN_CENTER|wx.ALL, 5 )
		
		m_choice_bytesizeChoices = []
		self.m_choice_bytesize = wx.Choice( self.m_panel1, wx.ID_ANY, wx.DefaultPosition, wx.Size( 100,-1 ), m_choice_bytesizeChoices, 0 )
		self.m_choice_bytesize.SetSelection( 0 )
		gSizer3.Add( self.m_choice_bytesize, 0, wx.ALIGN_CENTER|wx.ALL, 5 )
		
		self.m_staticText6 = wx.StaticText( self.m_panel1, wx.ID_ANY, u"停止位", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText6.Wrap( -1 )
		gSizer3.Add( self.m_staticText6, 0, wx.ALIGN_CENTER|wx.ALL, 5 )
		
		m_choice_stopbitChoices = []
		self.m_choice_stopbit = wx.Choice( self.m_panel1, wx.ID_ANY, wx.DefaultPosition, wx.Size( 100,-1 ), m_choice_stopbitChoices, 0 )
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
	

