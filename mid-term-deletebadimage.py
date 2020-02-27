# -*- coding: utf-8 -*-
"""
Created on Wed Apr 24 19:48:13 2019

@author: anktkyo
"""

from urllib import request
import time
import imghdr
import os

savepath='./images/'           #图片保存到的文件夹路径

imagecount=0
total=2700
for i in range(0,total):
    if imagecount>total:
        break
    try:
        imagepath=savepath+str(imagecount)+'.jpg'     #每一张图片的路径
        if os.path.exists(imagepath):
            print("%d,Image Exists" %i)
            isbad=imghdr.what(imagepath)
            if isbad==None:
                print("%d,Image is wrong" %i)
                os.remove(imagepath)
                print("%d,Image deleted" %i)
        else:
            print("%d,Image does not exist" %i)
            
        imagecount=imagecount+1
    except :
        print("%d,Wrong to Delete!" %i)                 
        continue             