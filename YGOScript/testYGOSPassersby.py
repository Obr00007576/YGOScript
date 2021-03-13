# coding=utf-8
from difflib import restore
from sys import flags
from airtest.core.api import *
from airtest.aircv import *
import pywinauto
from pywinauto import *
import unittest
import pytesseract
import cv2
import win32api,win32gui,win32con
import logging
logger = logging.getLogger("airtest")
logger.setLevel(logging.ERROR)

def no_double_click_time():
    return 0
win32gui.GetDoubleClickTime = no_double_click_time

#get processed image to get well-recognized results of words in image
def preprocessImg(image):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]
    return thresh

class testYGOScript(unittest.TestCase):
    #app to control
    dev=None
    @staticmethod
    def isInRect(pos,rect):
        if pos[0]>=rect[0] and pos[1]>=rect[1] and pos[0]<=rect[2] and pos[1]<=rect[3]:
            return True
        return False
        
    @staticmethod
    def my_exists(v):
        try:
            pos = loop_find(v, timeout=0.2,interval=0.1)
        except TargetNotFoundError:
            return False
        else:
            return pos
    
    @staticmethod
    def wait_text(text,rect):
        for n in range(0,30):
            if testYGOScript.exists_text(text,rect):
                assert(True)
                return
            sleep(0.3)
        assert(False)

    @staticmethod
    def exists_text(text,rect):
        img=crop_image(testYGOScript.dev.snapshot(),rect)
        img=preprocessImg(img)
        textImg=pytesseract.image_to_string(img,lang="eng",config="--psm 7 --oem 3")
        if text in textImg:
            return True
        return False
        
    @staticmethod
    def press(cursor_pos=[0,0],stop=False):
        if stop==False:
            cursor_pos[0]=cursor_pos[0]+testYGOScript.dev.get_pos()[0]
            cursor_pos[1]=cursor_pos[1]+testYGOScript.dev.get_pos()[1]
            testYGOScript.dev.mouse.click(coords=cursor_pos)
        else:
            testYGOScript.dev.mouse.click(coords=win32api.GetCursorPos())
    
    @staticmethod
    def my_swipe(pos1,pos2):
        wpos=testYGOScript.dev.get_pos()
        realPos1=[pos1[0]+wpos[0],pos1[1]+wpos[1]]
        realPos2=[pos2[0]+wpos[0],pos2[1]+wpos[1]]
        testYGOScript.dev.mouse.press(button="left",coords=realPos1)
        sleep(0.1)
        testYGOScript.dev.mouse.move(tuple(realPos2))
        sleep(0.2)
        testYGOScript.dev.mouse.release(button="left",coords=realPos2)

    @staticmethod
    def my_scroll():
        testYGOScript.dev.mouse.scroll(coords=(842+testYGOScript.dev.get_pos()[0], 522+testYGOScript.dev.get_pos()[1]), wheel_dist=3)

    @staticmethod
    def skip_talk():
        sleep(0.5)
        while(True):
            area_img=crop_image(testYGOScript.dev.snapshot(),[1166,944,1171,949])
            for line in area_img:
                for pix in line:
                    if pix[0]!=255 or pix[1]!=255 or pix[2]!=255:
                        return
            testYGOScript.press(cursor_pos=[817,877])

#preparation for the tests later - to set the dev as the application
class testBeforeScript(testYGOScript):
    def testBeforeScript(self):
        hwnd=findwindows.find_windows(title_re="Yu-Gi-Oh! DUEL LINKS")[0]
        testYGOScript.dev=init_device(platform="Windows",uuid=hwnd)
        win32gui.ShowWindow(hwnd, win32con.SW_MINIMIZE)
        win32gui.ShowWindow(hwnd, win32con.SW_RESTORE)
        #connect_device("Windows:///"+str(findwindows.find_windows(title_re="Yu-Gi-Oh! DUEL LINKS")[0]))

class testFindKey(testYGOScript):
    def testFindKey(self):
        pos=exists(Template(r"imgFindKey\\1.JPG"))
        if pos:
            touch(pos)
        wait(Template(r"imgFindKey\\2.JPG"))
        pos=exists(Template(r"imgFindKey\\2.JPG"))
        if pos:
            touch(pos)
        assert(True)

class testFindPasserby(testYGOScript):
    area_rect=(631,491,1062,866)
    def recognizeFaces():
        cascade = cv2.CascadeClassifier("lbpcascade_animeface.xml")
        img=crop_image(testYGOScript.dev.snapshot(),testFindPasserby.area_rect)
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        gray = cv2.equalizeHist(gray)
        faces=list(cascade.detectMultiScale(gray,scaleFactor = 1.1,minNeighbors = 5,minSize = (24, 24),flags=cv2.CASCADE_DO_ROUGH_SEARCH))
        if not faces:
            return []
        else:
            globfaces=[]
            for [x,y,w,h] in faces:
                globfacepos=[x+w/2+testFindPasserby.area_rect[0],y+h/2+testFindPasserby.area_rect[1]]
                globfaces.append(globfacepos)
            return globfaces


    def testFindPasserby(self):
        while True:
            facepos=None
            for pos in testFindPasserby.recognizeFaces():
                cond1=not testYGOScript.isInRect(pos,[635,490,737,632]) or not testYGOScript.exists_text("Gate",[577,945,630,962])
                cond2=not testYGOScript.isInRect(pos,[737,616,778,668]) or not testYGOScript.exists_text("PvP Arena",[719,944,801,961])
                if pos and cond1 and cond2:
                    facepos=pos
                    break
            if facepos!=None:
                touch(facepos)
                break
            testYGOScript.my_scroll()
            sleep(2.5)
        testYGOScript.skip_talk()
        testYGOScript.wait_text("Auto-Duel",[944,829,1082,859])
        touch([1011,843])
        while(not testYGOScript.exists_text("OK",[805,900,874,931])):
            sleep(0.2)
        if testYGOScript.exists_text("OK",[809,900,874,931]):
            touch([838,915])
        while(True):
            for i in range(0,3):
                testYGOScript.press(cursor_pos=[497,821])
            if testYGOScript.exists_text("NEXT",[779,892,893,938]):
                touch([842,917])
            pos=testYGOScript.my_exists(Template(r"imgFindPasserby\\2.JPG"))
            if pos:
                touch(pos)
            if testYGOScript.exists_text("Information",[1197,36,1312,60]):
                break
if __name__=="__main__":
    suite=unittest.TestSuite()
    suite.addTest(testBeforeScript("testBeforeScript"))
    unittest.TextTestRunner().run(suite)
    while(True):
        suite=unittest.TestSuite()
        suite.addTest(testFindPasserby("testFindPasserby"))
        unittest.TextTestRunner().run(suite)