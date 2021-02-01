from airtest.core.api import *
from airtest.aircv import *
from pywinauto import*
from tkinter import *
import pytesseract
import win32api

def preprocessImg(image):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]
    return thresh
state_release=0x00
prestate=win32api.GetKeyState(0x01)
tk=Tk()
dev=init_device(platform="Windows",uuid=findwindows.find_windows(title_re="Yu-Gi-Oh! DUEL LINKS")[0])
dev.set_foreground()
dev_pos=dev.get_pos()
tk.attributes("-alpha", 0.3)
tk.attributes("-topmost", True)
tk.geometry("1664x936"+"+"+str(dev_pos[0])+"+"+str(dev_pos[1]))
while True:
    tk.update_idletasks()
    tk.update()
    state=win32api.GetKeyState(0x01)
    if state!=state_release:
        if state < 0 and state!=prestate:
            cursor_pos=win32api.GetCursorPos()
            print(cursor_pos[0]-dev_pos[0],cursor_pos[1]-dev_pos[1])
            tk.destroy()
            break
    prestate=state
    time.sleep(0.01)