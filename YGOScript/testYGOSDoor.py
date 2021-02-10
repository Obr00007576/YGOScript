# coding=utf-8
from airtest.core.api import *
from airtest.aircv import *
from pywinauto import*
import pytesseract
import unittest
import win32api,win32gui,win32con
import logging

logger = logging.getLogger("airtest")
logger.setLevel(logging.NOTSET)
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

    #self-defined exsits() to have shorter interval and timeout
    @staticmethod
    def my_exists(v):
        try:
            pos = loop_find(v, timeout=0.2,interval=0.1)
        except TargetNotFoundError:
            return False
        else:
            return pos
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
        for n in range(0,100):
            if testYGOScript.exists_text(text,rect):
                return
            sleep(0.3)

    #simulate the press action in the window without limit of interval of click
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
    def skip_talk():
        flag=False
        while True:
            area_img=crop_image(testYGOScript.dev.snapshot(),[1166,944,1169,947])
            for line in area_img:
                for pix in line:
                    if pix[0]==255 and pix[1]==255 and pix[2]==255:
                        flag=True
            if flag:
                break
        while True:
            area_img=crop_image(testYGOScript.dev.snapshot(),[1166,944,1169,947])
            for line in area_img:
                for pix in line:
                    if pix[0]!=255 or pix[1]!=255 or pix[2]!=255:
                        return
            testYGOScript.press(cursor_pos=[817,877])

#preparation for the tests later - to set the dev as the application
class testBeforeScript(testYGOScript):
    def testBeforeScript():
        hwnd=findwindows.find_windows(title_re="Yu-Gi-Oh! DUEL LINKS")[0]
        testYGOScript.dev=init_device(platform="Windows",uuid=hwnd)
        win32gui.ShowWindow(hwnd, win32con.SW_MINIMIZE)
        win32gui.ShowWindow(hwnd, win32con.SW_RESTORE)
        #connect_device("Windows:///"+str(findwindows.find_windows(title_re="Yu-Gi-Oh! DUEL LINKS")[0]))

#steps of entering the door
class testEnterTheDoor(testYGOScript):
    def testEnterTheDoor():
        if testYGOScript.exists_text("Information",[1197,36,1312,60]):
            touch([947,440])
        wait(Template(r"imgEnterTheDoor\\2.JPG"))
        pos=exists(Template(r"imgEnterTheDoor\\2.JPG"))
        if pos:
            touch(pos)
        sleep(0.5)
        testYGOScript.skip_talk()
        wait(Template(r"imgEnterTheDoor\\2.JPG"))
        pos=exists(Template(r"imgEnterTheDoor\\2.JPG"))
        if pos:
            touch(pos)
        while True:
            if testYGOScript.exists_text("Your Main Phase",[937,79,1107,103]) or testYGOScript.exists_text("Your Draw Phase",[937,79,1107,103]):
                break
            testYGOScript.press(cursor_pos=[817,516])
        sleep(0.5)

#steps of battle
class testDueling(testYGOScript):
    ATKrects=[[792,593,826,611],[899,593,933,610],[685,594,717,612]]
    SwipePos=[[[839,583],[839,450]],[[950,583],[950,450]],[[732,583],[732,450]]]
    
    #operations of your draw phase
    def testDrawPhase():
        if testYGOScript.exists_text("Your Draw Phase",[937,79,1107,103]):
            sleep(1)
            for i in range(0,9):
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
        if testYGOScript.exists_text("TK",testDueling.ATKrects[boardIndex]):
            testYGOScript.my_swipe(testDueling.SwipePos[boardIndex][0],testDueling.SwipePos[boardIndex][1])
            for i in range(0,2):
                sleep(0.1)
                testYGOScript.press(stop=True)
            sleep(1.1)
            if testYGOScript.exists_text("LP: O",[1572,854,1659,898]) or testYGOScript.exists_text("LP: o",[1572,854,1659,898]):
                while(not testYGOScript.exists_text("OK",[809,900,874,931])):
                    sleep(0.2)
                if testYGOScript.exists_text("OK",[809,900,874,931]):
                    touch([838,915])
                return True
        return False
    
    #dueling
    def testDueling():
        for i in range(0,15):
            if testYGOScript.exists_text("Your Main Phase",[937,79,1107,103]):
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
    def testEnd():
        while(True):
            for i in range(0,3):
                testYGOScript.press(cursor_pos=[844,832])
            if testYGOScript.exists_text("NEXT",[751,899,915,934]):
                touch([840,919])
            pos=testYGOScript.my_exists(Template(r"imgEnd\\1.JPG"))
            if pos:
                touch(pos)
            if testYGOScript.exists_text("Information",[1197,36,1312,60]):
                break

if __name__=="__main__":
    testBeforeScript.testBeforeScript()
    while True:
        testEnterTheDoor.testEnterTheDoor()
        testDueling.testDueling()
        testEnd.testEnd()