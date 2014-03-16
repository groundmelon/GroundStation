/*
 *	文件组织结构介绍以及各个文件功能的介绍。详细介绍见各个源码里的注释。
 */

Folder PATH listing for volume Usage        
Volume serial number is 0000006E 8484:C04C  
F:.                                         //GUI模块文件夹
│  .project                                 
│  .pydevproject                            
│  ButtonBase.py							//按钮部分的绑定函数和逻辑处理函数
│  GroundStation.py							//主类
│  GroundStationBase.py                     //主类的基类，由GUI设计软件生成
│  ImageShow.py                             //独立窗口类
│  ImageShowBase.py                         //独立窗口基类
│  Menu.py                                  //菜单部分的绑定函数和逻辑处理函数
│  PickleFileIO.py                          //文件读取接口
│  ReadMe.txt                               //说明文档
│  SerialReceiverThread.py                  //串口接受线程
│  SerialSettingDialog.py                   //串口设置对话框
│  TraceBase.py                             //跟踪模块的绑定函数和逻辑处理函数
│  util.py                                  //通用工具接口
│                                           
├─.settings                                 
│      org.eclipse.core.resources.prefs     
│                                           
├─attitude                                  //姿态处理模块文件夹
│      attitudeMod.py                       //姿态处理模块
│      draw.py                              //绘制所需的资源文件的绘图脚本
│      empty.bmp                            //空图片
│      panel.bmp                            //表盘图片
│      panel_white.bmp                      
│      pmask.bmp                            //表盘掩码图片
│      __init__.py                          
│                                           
├─communication                             //通信模块文件夹
│      xbee.gss                             //xbee默认设置文件
│      XBeeComm.py                          //xbee通信模块
│      __init__.py                          
│                                           
├─GUIDesign                                 //GUI设置文件夹
│      ground_station_design.fbp            //
│      ImageShowFrame.fbp                   //
│                                           
├─imageprocess                              //图像处理文件夹
│      cvtest.py                            //opencv测试脚本
│      ipythonutil.py                       //调试工具ipythonutil
│      lena.jpg                             //测试用文件
│      test.py                              //图像处理测试文件
│                                           
├─old                                       //废弃文件
│      Button.py                            
│      Trace.py.old                         
│                                           
└─resources                                 //资源文件夹
        null.bmp                            //无信号图像
        
