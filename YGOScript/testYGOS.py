# coding=utf-8
from airtest.core.api import *
from airtest.aircv import *
from pywinauto import*
import pytesseract
import unittest
import win32api
import win32gui

def no_double_click_time():
    return 0
win32gui.GetDoubleClickTime = no_double_click_time

def rotate_image(image, angle):
  image_center = tuple(np.array(image.shape[1::-1]) / 2)
  rot_mat = cv2.getRotationMatrix2D(image_center, angle, 1.0)
  result = cv2.warpAffine(image, rot_mat, image.shape[1::-1], flags=cv2.INTER_LINEAR)
  return result

def preprocessImg(image):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]
    return thresh

class testYGOScript(unittest.TestCase):
    dev=None
    @staticmethod
    def exists_text(text,rect,angle=0):
        img=crop_image(testYGOScript.dev.snapshot(),rect)
        if angle!=0:
            img=rotate_image(img,angle)
        img=preprocessImg(img)
        textImg=pytesseract.image_to_string(img,lang="eng",config="--psm 7 --oem 3")
        print(textImg)
        if text in textImg:
            return True
        return False
    @staticmethod
    def wait_text(text,rect):
        for n in range(0,12):
            if testYGOScript.exists_text(text,rect):
                assert(True)
                return
            sleep(1)
        assert(False)

    @staticmethod
    def press(cursor_pos=[0,0],stop=False):
        if stop==False:
            cursor_pos[0]=cursor_pos[0]+testYGOScript.dev.get_pos()[0]
            cursor_pos[1]=cursor_pos[1]+testYGOScript.dev.get_pos()[1]
            testYGOScript.dev.mouse.click(coords=cursor_pos)
        else:
            testYGOScript.dev.mouse.click(coords=win32api.GetCursorPos())

    def testBeforeScript(self):
        testYGOScript.dev=init_device(platform="Windows",uuid=findwindows.find_windows(title_re="Yu-Gi-Oh! DUEL LINKS")[0])
        testYGOScript.dev.set_foreground()
        #connect_device("Windows:///"+str(findwindows.find_windows(title_re="Yu-Gi-Oh! DUEL LINKS")[0]))
        assert(True)

    def testEnterTheDoor(self):
        wait(Template(r"imgEnterTheDoor\\1.JPG"))
        pos=exists(Template(r"imgEnterTheDoor\\1.JPG"))
        if pos:
            touch(pos)
        wait(Template(r"imgEnterTheDoor\\2.JPG"))
        pos=exists(Template(r"imgEnterTheDoor\\2.JPG"))
        if pos:
            touch(pos)
        sleep(0.5)
        for i in range(0,5):
            sleep(0.2)
            testYGOScript.press([839,583])
        wait(Template(r"imgEnterTheDoor\\2.JPG"))
        pos=exists(Template(r"imgEnterTheDoor\\2.JPG"))
        if pos:
            touch(pos)
        for i in range(40):
            sleep(0.2)
            testYGOScript.press([839,583])
        sleep(2.5)
        assert(True)

    def testDueling(self):
        for i in range(0,15):
            if testYGOScript.exists_text("1",[1051,41,1078,73]) and  testYGOScript.exists_text("Your Main Phase",[937,79,1107,103]):
                if testYGOScript.exists_text("Your Main Phase",[937,79,1107,103]):
                    testYGOScript.dev.touch([830,906])
                    wait(Template(r"imgDueling\\1.JPG"))
                    pos=exists(Template(r"imgDueling\\1.JPG"))
                    if pos:
                        touch(pos)
                    pos=exists(Template(r"imgDueling\\2.JPG"))
                    if pos:
                        touch(pos)
                    sleep(0.1)
                    touch(pos)
            else:
                testYGOScript.wait_text("Your Draw Phase",[937,79,1107,103])
                if testYGOScript.exists_text("Your Draw Phase",[937,79,1107,103]):
                    sleep(0.5)
                    for i in range(0,9):
                        sleep(0.1)
                        testYGOScript.press([834,506])
                testYGOScript.wait_text("Your Main Phase",[937,79,1107,103])
                if testYGOScript.exists_text("Your Main Phase",[937,79,1107,103]):
                    if not testYGOScript.exists_text("ATK",[899,593,933,610]):
                        testYGOScript.dev.touch([830,906])
                        wait(Template(r"imgDueling\\1.JPG"))
                        pos=exists(Template(r"imgDueling\\1.JPG"))
                        if pos:
                            touch(pos)
                    wait(Template(r"imgDueling\\2.JPG"))
                    pos=exists(Template(r"imgDueling\\2.JPG"))
                    if pos:
                        touch(pos)
                        sleep(0.1)
                        touch(pos)
                testYGOScript.wait_text("Your Battle Phase",[937,79,1107,103])
                if testYGOScript.exists_text("Your Battle Phase",[937,79,1107,103]):
                    if testYGOScript.exists_text("ATK",[792,593,826,611]):
                        swipe([839,583],[839,475],duration=0.01,steps=1)
                        testYGOScript.press(stop=True)
                        testYGOScript.press(stop=True)
                        sleep(1)
                        if testYGOScript.exists_text(": O",[1572,854,1659,898]) or testYGOScript.exists_text(": o",[1572,854,1659,898]):
                            testYGOScript.wait_text("OK",[809,900,874,931])
                            touch([843,919])
                            return
                    if testYGOScript.exists_text("ATK",[899,593,933,610]):
                        swipe([948,583],[948,475],duration=0.01,steps=1)
                        testYGOScript.press(stop=True)
                        testYGOScript.press(stop=True)
                        sleep(1)
                        if testYGOScript.exists_text(": O",[1572,854,1659,898]) or testYGOScript.exists_text(": o",[1572,854,1659,898]):
                            testYGOScript.wait_text("OK",[809,900,874,931])
                            touch([843,919])
                            return
                    if testYGOScript.exists_text("ATK",[685,594,717,612]):
                        swipe([732,583],[732,475],duration=0.01,steps=1)
                        testYGOScript.press(stop=True)
                        testYGOScript.press(stop=True)
                        sleep(1)
                        if testYGOScript.exists_text(": O",[1572,854,1659,898]) or testYGOScript.exists_text(": o",[1572,854,1659,898]):
                            testYGOScript.wait_text("OK",[809,900,874,931])
                            touch([843,919])
                            return
                    wait(Template(r"imgDueling\\2.JPG"))
                    pos=exists(Template(r"imgDueling\\2.JPG"))
                    if pos:
                        touch(pos)
                        sleep(0.1)
                        touch(pos)
                    sleep(3)
    
    def testEnd(self):
        testYGOScript.wait_text("NEXT",[798,900,878,933])
        touch([840,933])
        for i in range(0,15):
            sleep(0.1)
            testYGOScript.press(stop=True)
        wait(Template(r"imgEnd\\1.JPG"))
        pos=exists(Template(r"imgEnd\\1.JPG"))
        if pos:
            touch(pos)
        for i in range(0,14):
            sleep(0.1)
            testYGOScript.press(stop=True)
        pos=exists(Template(r"imgEnd\\1.JPG"))
        if pos:
            touch(pos)


if __name__=="__main__":
    suite=unittest.TestSuite()
    suite.addTests([testYGOScript("testBeforeScript")])
    unittest.TextTestRunner().run(suite)
    while(True):
        suite=unittest.TestSuite()
        suite.addTests([testYGOScript("testEnterTheDoor"),testYGOScript("testDueling"),testYGOScript("testEnd")])
        unittest.TextTestRunner().run(suite)