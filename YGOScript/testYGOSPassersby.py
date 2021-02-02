# coding=utf-8
from airtest.core.api import *
from airtest.aircv import *
from pywinauto import*
import unittest

class testYGOScript(unittest.TestCase):
    #app to control
    dev=None

#preparation for the tests later - to set the dev as the application
class testBeforeScript(testYGOScript):
    def testBeforeScript(self):
        testYGOScript.dev=init_device(platform="Windows",uuid=findwindows.find_windows(title_re="Yu-Gi-Oh! DUEL LINKS")[0])
        testYGOScript.dev.set_foreground()
        #connect_device("Windows:///"+str(findwindows.find_windows(title_re="Yu-Gi-Oh! DUEL LINKS")[0]))
        assert(True)

class testFindKey(testYGOScript):
    def testFindKeys(self):
        pos=exists(Template(r"imgFindKey\\1.JPG"))
        if pos:
            touch(pos)
        wait(Template(r"imgFindKey\\2.JPG"))
        pos=exists(Template(r"imgFindKey\\2.JPG"))
        if pos:
            touch(pos)
        assert(True)

class testFindPasserby(testYGOScript):
    def testFindPasserby(self):
        pos=exists(Template(r"imgFindPasserby\\p8.JPG"))
        if pos:
            touch(pos)
        # wait(Template(r"imgFindPasserby\\1.JPG"))
        # pos=exists(Template(r"imgFindPasserby\\1.JPG"))
        # if pos:
        #     touch(pos)

if __name__=="__main__":
    suite=unittest.TestSuite()
    suite.addTests([testBeforeScript("testBeforeScript"),testFindPasserby("testFindPasserby")])
    unittest.TextTestRunner().run(suite)