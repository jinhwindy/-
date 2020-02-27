# -*- coding: utf-8 -*-
"""
Created on Thu Apr 25 15:24:57 2019

@author: anktkyo
"""

from urllib import request
import random
import shutil
import os

originpath='./choose_images/'           #图片来源到的文件夹路径
newpath='./histogram_images/'       #图片保存到的文件夹路径

imagecount=0
indexmax=2700
total=78   #选择500张
for i in range(0,1000):
    if imagecount>total:
        break
    try:
        randomindex=random.randint(0,indexmax)
        print(randomindex)
        imagepath=originpath+str(randomindex)+'.jpg'     #随机图片的路径
        savepath=newpath+str(randomindex)+'.jpg'  #保存路径
        if os.path.exists(imagepath):
            print("%d,Image Exists" %randomindex)
            if os.path.exists(savepath):
                print("%d,Already Exist" %randomindex)
            else:
                shutil.copy(imagepath,savepath)
                print("%d,copy OK" %randomindex)
                imagecount=imagecount+1

        else:
            print("%d,Image does not exist" %randomindex)
             
    except :
        print("%d,Wrong to copy!" %randomindex)                 
        continue             