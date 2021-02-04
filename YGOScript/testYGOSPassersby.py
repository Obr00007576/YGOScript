# coding=utf-8
from sys import flags
from airtest.core.api import *
from airtest.aircv import *
from pywinauto import*
import unittest
import pytesseract
import cv2
import win32gui
import win32api
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
        testYGOScript.dev.mouse.press(button="left",coords=pos1)
        sleep(0.1)
        testYGOScript.dev.mouse.release(button="left",coords=pos2)

#preparation for the tests later - to set the dev as the application
class testBeforeScript(testYGOScript):
    def testBeforeScript(self):
        testYGOScript.dev=init_device(platform="Windows",uuid=findwindows.find_windows(title_re="Yu-Gi-Oh! DUEL LINKS")[0])
        testYGOScript.dev.set_foreground()
        #connect_device("Windows:///"+str(findwindows.find_windows(title_re="Yu-Gi-Oh! DUEL LINKS")[0]))
        assert(True)

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
    area_rect=(724,550,1057,839)
    def recognizeFaces():
        cascade = cv2.CascadeClassifier("lbpcascade_animeface.xml")
        img=crop_image(testYGOScript.dev.snapshot(),testFindPasserby.area_rect)
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        gray = cv2.equalizeHist(gray)
        faces=list(cascade.detectMultiScale(gray,scaleFactor = 1.1,minNeighbors = 5,minSize = (24, 24),flags=cv2.CASCADE_DO_ROUGH_SEARCH))
        if not faces:
            return ()
        else:
            [x,y,w,h] = faces[0]
            return [x+w/2+724,y+h/2+550]

    def testFindPasserby(self):
        while True:
            pos=testFindPasserby.recognizeFaces()
            if pos:
                touch(pos)
                break
            else:
                testYGOScript.my_swipe([1020,561],[780,561])
                sleep(2.5)
        for i in range(0,9):
            testYGOScript.press(cursor_pos=[839,583])
            sleep(0.2)
        wait(Template(r"imgFindPasserby\\1.JPG"))
        pos=exists(Template(r"imgFindPasserby\\1.JPG"))
        if pos:
            touch(pos)
        while(not testYGOScript.exists_text("OK",[809,900,874,931])):
            sleep(0.2)
        pos=testYGOScript.exists_text("OK",[809,900,874,931])
        if pos:
            touch([843,919])
        testYGOScript.wait_text("NEXT",[798,900,878,933])
        pos=testYGOScript.exists_text("NEXT",[798,900,878,933])
        if pos:
            touch([840,933])
        while(True):
            for i in range(0,8):
                sleep(0.1)
                testYGOScript.press(stop=True)
            pos=testYGOScript.my_exists(Template(r"imgFindPasserby\\2.JPG"))
            if pos:
                touch(pos)
            if testYGOScript.exists_text("Information",[1197,36,1312,60]):
                break

if __name__=="__main__":
    suite=unittest.TestSuite()
    suite.addTests([testBeforeScript("testBeforeScript")])
    unittest.TextTestRunner().run(suite)
    while(True):
        suite=unittest.TestSuite()
        suite.addTest(testFindPasserby("testFindPasserby"))
        unittest.TextTestRunner().run(suite)