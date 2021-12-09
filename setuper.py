import sys
from cx_Freeze import setup, Executable

# Dependencies are automatically detected, but it might need fine tuning.
build_exe_options = {"packages": ["os","numpy"], "includes": ["numpy"], "excludes": ["tkinter"], "include_files":["AIRLab_logo.jpg"]}

# GUI applications require a different base on Windows (the default is for
# a console application).
base = None
if sys.platform == "win32":
        base = "Win32GUI"

setup(  name = "AIRlab",
        version = "0.1",
        description = "AIRlab Olfactortmeter",
        options = {"build_exe": build_exe_options},
        executables = [Executable("main.py", base=base, icon="AIRLab_logo.ico")])


# python3 setuper.py build
# MacOS python3 setuper.py bdist_dmg
# Windows python3 setuper.py bdist_msi

# pyuic5 ui_main.ui -o ui_main.py