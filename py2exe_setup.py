# -*- coding: utf-8 -*- 
# setup.py 
from distutils.core import setup
import py2exe
includes = ["encodings", "encodings.*"]

manifest = ''' 
        <assembly xmlns="urn:schemas-microsoft-com:asm.v1" 
        manifestVersion="1.0"> 
        <assemblyIdentity 
        version="0.6.8.0" 
        processorArchitecture="x86" 
        name="YourApp" 
        type="win32" 
        /> 
        <description>YourApp</description> 
        <trustInfo xmlns="urn:schemas-microsoft-com:asm.v3"> 
        <security> 
        <requestedPrivileges> 
        <requestedExecutionLevel 
        level="asInvoker" 
        uiAccess="false" 
        /> 
        </requestedPrivileges> 
        </security> 
        </trustInfo> 
        <dependency> 
        <dependentAssembly> 
        <assemblyIdentity 
        type="win32" 
        name="Microsoft.VC90.CRT" 
        version="9.0.21022.8" 
        processorArchitecture="x86" 
        publicKeyToken="1fc8b3b9a1e18e3b" 
        /> 
        </dependentAssembly> 
        </dependency> 
        <dependency> 
        <dependentAssembly> 
        <assemblyIdentity 
        type="win32" 
        name="Microsoft.Windows.Common-Controls" 
        version="6.0.0.0" 
        processorArchitecture="x86" 
        publicKeyToken="6595b64144ccf1df" 
        language="*" 
        /> 
        </dependentAssembly> 
        </dependency> 
        </assembly> 
        '''
options = {"py2exe":
            {   "compressed": 1,
                "optimize": 2,
                "includes": includes,
                "bundle_files": 3
            }
          }
setup(   
    version = "1.0.0",
    description = "GroundStation@GroundMelon",
    name = "GroundStation",
    options = options,
    zipfile=None,
    windows=[{"script": "GroundStation.py",
              "icon_resources": [(1, r"resources/gs.ico")],
              "other_resources":[(24,1,manifest)]
              }],  
    )
