# -*- coding: GBK -*-
from airtest.core.api import *
from airtest.aircv import *
from pywinauto import*
from tkinter import *
import pytesseract
import win32api,win32gui,win32con

def rotate_image(image, angle):
  image_center = tuple(np.array(image.shape[1::-1]) / 2)
  rot_mat = cv2.getRotationMatrix2D(image_center, angle, 1.0)
  result = cv2.warpAffine(image, rot_mat, image.shape[1::-1], flags=cv2.INTER_LINEAR)
  return result

def preprocessImg(image):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]
    return thresh
state_release=0x00
prestate=win32api.GetKeyState(0x01)
tk=Tk()
hwnd=findwindows.find_windows(title_re="Yu-Gi-Oh! DUEL LINKS")[0]
dev=init_device(platform="Windows",uuid=hwnd)
win32gui.ShowWindow(hwnd, win32con.SW_MINIMIZE)
win32gui.ShowWindow(hwnd, win32con.SW_RESTORE)
dev_pos=dev.get_pos()
tk.attributes("-alpha", 0.3)
tk.attributes("-topmost", True)
tk.geometry("1664x936"+"+"+str(dev_pos[0])+"+"+str(dev_pos[1]))
snapshot_rect=[]
n=0
while True:
    tk.update_idletasks()
    tk.update()
    state=win32api.GetKeyState(0x01)
    if state!=state_release:
        if state < 0 and state!=prestate:
            n+=1
            cursor_pos=win32api.GetCursorPos()
            print(cursor_pos[0]-dev_pos[0],cursor_pos[1]-dev_pos[1])
            snapshot_rect.append(cursor_pos[0]-dev_pos[0])
            snapshot_rect.append(cursor_pos[1]-dev_pos[1])
            if n==2:
                tk.destroy()
                break
    prestate=state
    time.sleep(0.01)
area_img=crop_image(dev.snapshot(),snapshot_rect)
img=preprocessImg(area_img)
print(pytesseract.image_to_string(img,config="--psm 7 --oem 3"))
show_origin_size(img,"asd")