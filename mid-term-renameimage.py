# -*- coding: utf-8 -*-
"""
Created on Thu Apr 25 15:24:57 2019

@author: anktkyo
"""


import os


newpath='./histogram_images/'       #图片保存到的文件夹路径
imagelist=os.listdir(newpath)  #获取图像名称列表
total=len(imagelist)

index=0

for item in imagelist:
    src=newpath+item
    dst=newpath+str(index)+'h.jpg'
    try:
        os.rename(src,dst)
        print("Rename OK")
        index=index+1
    except:
        print('wrong')
        continue

print("Rename Total %d" %(index+1))