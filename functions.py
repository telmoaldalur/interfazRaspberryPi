import ctypes  # An included library with Python install.

MB_OK = 0x0
MB_OKCXL = 0x01
MB_YESNOCXL = 0x03
MB_YESNO = 0x04
MB_HELP = 0x4000
ICON_EXLAIM=0x30
ICON_INFO = 0x40
ICON_STOP = 0x10

def Mbox(title, text, style):
    ctypes.windll.user32.MessageBoxA(0, text, title, style)
