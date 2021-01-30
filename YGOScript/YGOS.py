# coding=utf-8
from airtest.core.api import *
from airtest.aircv import *
from pywinauto import*

dev=init_device(platform="Windows",uuid=findwindows.find_windows(title_re="Yu-Gi-Oh! DUEL LINKS")[0])
#connect_device("Windows:///"+str(findwindows.find_windows(title_re="Yu-Gi-Oh! DUEL LINKS")[0]))
touch([100,100])
a=crop_image(dev.snapshot(),[400,400,600,600])
show_origin_size(a,title="asd")