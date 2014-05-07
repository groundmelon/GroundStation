# -*- coding: utf-8 -*- 
'''
Created on 2013-12-8

@author: GroundMelon
'''
from IPython.terminal.embed import InteractiveShellEmbed
from IPython import embed
import os
if os.getenv('IPYTHONDBG'):
    print('IPythonDebug ON')
    ipshell = InteractiveShellEmbed(banner1 = 'IPython Shell',
                           exit_msg = 'Exit IPython Shell')
    def embed():
        embed()
else:
    print('IPythonDebug OFF')
    def foo():
        pass
    ipshell = foo
    embed = foo
