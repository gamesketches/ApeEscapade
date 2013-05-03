from cx_Freeze import setup, Executable
import sys

#productName = "ApeEscapade"
#if 'bdist_msi' in sys.argv:
#    sys.argv += ['--initial-target-dir', 'C:\InstallDir\\' + productName]
#    sys.argv += ['--install-script', 'install.py']
#
#exe = Executable(
#      script="ApeEscapade.py",
#      base="Win32GUI",
#      targetName="ApeEscapade.exe"
#     )
setup(
      name="ApeEscapade.exe",
      version="1.0",
      author="Me",
      description="Copyright 2012",
      executables=[Executable(script = "ApeEscapade.py", base = "Win32GUI")],
      )
