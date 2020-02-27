# -*- coding: utf-8 -*-
"""
Created on Fri Apr 26 14:37:49 2019

@author: anktkyo
"""
from PIL import Image
import os

imgpath='./histogram_samesize/'           #图片来源到的文件夹路径
newpath='./histogram_samesize/'
imagelist=os.listdir(imgpath)         #获取图像名称列表
total=len(imagelist)

for item in imagelist:
    path=imgpath+item
    pathnew=newpath+item[:-4]+'.bmp'
    img=Image.open(path,'r')
    print(img.mode)
    if img.mode=='P':
        img=img.convert('RGB')
    imgbmp=img
    imgbmp.save(pathnew,'bmp')       