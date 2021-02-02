# coding=utf-8
from airtest.core.api import *
from airtest.aircv import *
from pywinauto import*
import pytesseract
import unittest
import win32api
import win32gui
#set no limit of interval of click
def no_double_click_time():
    return 0
win32gui.GetDoubleClickTime = no_double_click_time

#rotate the image to recognize words
def rotate_image(image, angle):
  image_center = tuple(np.array(image.shape[1::-1]) / 2)
  rot_mat = cv2.getRotationMatrix2D(image_center, angle, 1.0)
  result = cv2.warpAffine(image, rot_mat, image.shape[1::-1], flags=cv2.INTER_LINEAR)
  return result

#get processed image to get well-recognized results of words in image
def preprocessImg(image):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]
    return thresh

class testYGOScript(unittest.TestCase):
    #app to control
    dev=None
    #check whether the text is in the given fixed area of a rect
    @staticmethod
    def exists_text(text,rect,angle=0):
        img=crop_image(testYGOScript.dev.snapshot(),rect)
        if angle!=0:
            img=rotate_image(img,angle)
        img=preprocessImg(img)
        textImg=pytesseract.image_to_string(img,lang="eng",config="--psm 7 --oem 3")
        if text in textImg:
            return True
        return False
    #wait for the text to be in the the given fixed area of a rect
    @staticmethod
    def wait_text(text,rect):
        for n in range(0,30):
            if testYGOScript.exists_text(text,rect):
                assert(True)
                return
            sleep(0.3)
        assert(False)
    #simulate the press action in the window without limit of interval of click
    @staticmethod
    def press(cursor_pos=[0,0],stop=False):
        if stop==False:
            cursor_pos[0]=cursor_pos[0]+testYGOScript.dev.get_pos()[0]
            cursor_pos[1]=cursor_pos[1]+testYGOScript.dev.get_pos()[1]
            testYGOScript.dev.mouse.click(coords=cursor_pos)
        else:
            testYGOScript.dev.mouse.click(coords=win32api.GetCursorPos())

#preparation for the tests later - to set the dev as the application
class testBeforeScript(testYGOScript):
    def testBeforeScript(self):
        testYGOScript.dev=init_device(platform="Windows",uuid=findwindows.find_windows(title_re="Yu-Gi-Oh! DUEL LINKS")[0])
        testYGOScript.dev.set_foreground()
        #connect_device("Windows:///"+str(findwindows.find_windows(title_re="Yu-Gi-Oh! DUEL LINKS")[0]))
        assert(True)

#steps of entering the door
class testEnterTheDoor(testYGOScript):
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

#steps of battle
class testDueling(testYGOScript):
    ATKrects=[[792,593,826,611],[899,593,933,610],[685,594,717,612]]
    SwipePos=[[[839,583],[839,475]],[[950,583],[950,475]],[[732,583],[732,475]]]
    
    #operations of your draw phase
    def testDrawPhase():
        if testYGOScript.exists_text("Your Draw Phase",[937,79,1107,103]):
            sleep(1)
            for i in range(0,7):
                sleep(0.1)
                testYGOScript.press([834,506])
    
    #operations of your main phase
    def testMainPhase():
        if testYGOScript.exists_text("Your Main Phase",[937,79,1107,103]):
            if not testYGOScript.exists_text("ATK",testDueling.ATKrects[2]):
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
    
    #operations of your battle phase
    def testBattlePhase():
        if testYGOScript.exists_text("Your Battle Phase",[937,79,1107,103]):
            for i in range(0,3):
                if testDueling.isAttackToLose(i):
                    return True
        wait(Template(r"imgDueling\\2.JPG"))
        pos=exists(Template(r"imgDueling\\2.JPG"))
        if pos:
            touch(pos)
            sleep(0.1)
            touch(pos)
        sleep(3)

        return False

    #check whether after this attack the enemy get 0 LP
    def isAttackToLose(boardIndex):
        if testYGOScript.exists_text("ATK",testDueling.ATKrects[boardIndex]):
            swipe(testDueling.SwipePos[boardIndex][0],testDueling.SwipePos[boardIndex][1],duration=0.01,steps=1)
            testYGOScript.press(stop=True)
            testYGOScript.press(stop=True)
            sleep(1)
            if testYGOScript.exists_text(": O",[1572,854,1659,898]) or testYGOScript.exists_text(": o",[1572,854,1659,898]):
                testYGOScript.wait_text("OK",[809,900,874,931])
                touch([843,919])
                return True
        return False
    
    #dueling
    def testDueling(self):
        for i in range(0,15):
            if testYGOScript.exists_text("1",[1051,41,1078,73]) and  testYGOScript.exists_text("Your Main Phase",[937,79,1107,103]):
                testDueling.testMainPhase()
            else:
                testYGOScript.wait_text("Your Draw Phase",[937,79,1107,103])
                testDueling.testDrawPhase()
                testYGOScript.wait_text("Your Main Phase",[937,79,1107,103])
                testDueling.testMainPhase()
                testYGOScript.wait_text("Your Battle Phase",[937,79,1107,103])
                if testDueling.testBattlePhase():
                    return

#steps to end the battle to the main interface
class testEnd(testYGOScript):
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
        for i in range(0,10):
            sleep(0.1)
            testYGOScript.press(stop=True)
        pos=exists(Template(r"imgEnd\\1.JPG"))
        if pos:
            touch(pos)

if __name__=="__main__":
    suite=unittest.TestSuite()
    suite.addTests([testBeforeScript("testBeforeScript")])
    unittest.TextTestRunner().run(suite)
    while(True):
        suite=unittest.TestSuite()
        suite.addTests([testEnterTheDoor("testEnterTheDoor"),testDueling("testDueling"),testEnd("testEnd")])
        unittest.TextTestRunner().run(suite)