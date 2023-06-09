import sys
from cx_Freeze import setup, Executable

base = None
if sys.platform == "win32":
    base = "Win32GUI"

setup(
    name = "To Do List",
    version = "0.1",
    description = "Sistema para gestão de tempo e afazeres",
    executables = [Executable("todolist.py", base=base)]
)