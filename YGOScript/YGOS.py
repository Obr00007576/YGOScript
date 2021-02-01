# coding=utf-8
from airtest.core.api import *
from airtest.aircv import *
from pywinauto import*
import pytesseract
import unittest
def preprocessImg(image):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]
    return thresh

class YGOTest(unittest.TestCase):
    @staticmethod
    def exists_text(text,rect):
        dev=device()
        img=crop_image(device().snapshot(),rect)
        img=preprocessImg(img)
        textImg=pytesseract.image_to_string(img,lang="eng",config="--psm 7 --oem 3")
        if text in textImg:
            return True
        return False
    @staticmethod
    def wait_text(text,rect):
        for n in range(0,12):
            if YGOTest.exists_text(text,rect):
                assert(True)
                return
            sleep(1)
        assert(False)

    def testBeforeScript(self):
        dev=init_device(platform="Windows",uuid=findwindows.find_windows(title_re="Yu-Gi-Oh! DUEL LINKS")[0])
        dev.set_foreground()
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
        wait(Template(r"imgEnterTheDoor\\2.JPG"))
        pos=exists(Template(r"imgEnterTheDoor\\2.JPG"))
        if pos:
            touch(pos)
        assert(True)
        sleep(10)
    def testDueling(self):
        for i in range(0,15):
            if YGOTest.exists_text("1",[1051,41,1078,73]) and  YGOTest.exists_text("Your Main Phase",[937,79,1107,103]):
                if YGOTest.exists_text("Your Main Phase",[937,79,1107,103]):
                    device().touch([830,906])
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
                YGOTest.wait_text("Your Draw Phase",[937,79,1107,103])
                sleep(1)
                if YGOTest.exists_text("Your Draw Phase",[937,79,1107,103]):
                    touch([834,506])
                    sleep(0.5)
                    touch([834,506])
                YGOTest.wait_text("Your Main Phase",[937,79,1107,103])
                if YGOTest.exists_text("Your Main Phase",[937,79,1107,103]):
                    if not YGOTest.exists_text("ATK",[685,594,717,609]) or not YGOTest.exists_text("ATK",[792,593,826,611]) or not YGOTest.exists_text("ATK",[899,593,933,610]):
                        device().touch([830,906])
                        wait(Template(r"imgDueling\\1.JPG"))
                        pos=exists(Template(r"imgDueling\\1.JPG"))
                        if pos:
                            touch(pos)
                    pos=exists(Template(r"imgDueling\\2.JPG"))
                    if pos:
                        touch(pos)
                    sleep(0.1)
                    touch(pos)
                YGOTest.wait_text("Your Battle Phase",[937,79,1107,103])
                if YGOTest.exists_text("Your Battle Phase",[937,79,1107,103]):
                    if YGOTest.exists_text("ATK",[685,594,717,612]):
                        swipe([732,583],[732,475],duration=0.01,steps=1)
                        sleep(1.5)
                        pos=exists(Template(r"imgDueling\\2.JPG"))
                        if pos==False:
                            YGOTest.wait_text("OK",[817,904,864,930])
                            touch([841,918])
                            return
                    if YGOTest.exists_text("ATK",[792,593,826,611]):
                        swipe([839,583],[839,475],duration=0.01,steps=1)
                        sleep(1.5)
                        pos=exists(Template(r"imgDueling\\2.JPG"))
                        if pos==False:
                            YGOTest.wait_text("OK",[817,904,864,930])
                            touch([841,918])
                            return                  
                    if YGOTest.exists_text("ATK",[899,593,933,610]):
                        swipe([948,583],[948,475],duration=0.01,steps=1)
                        sleep(1.5)
                        pos=exists(Template(r"imgDueling\\2.JPG"))
                        if pos==False:
                            YGOTest.wait_text("OK",[817,904,864,930])
                            touch([841,918])
                            return
                    pos=exists(Template(r"imgDueling\\2.JPG"))
                    if pos:
                        touch(pos)
                        sleep(0.1)
                        touch(pos)
                    sleep(3)

if __name__=="__main__":
    suite = unittest.TestSuite()
    suite.addTests([YGOTest("testBeforeScript"),YGOTest("testDueling")])
    unittest.TextTestRunner().run(suite)