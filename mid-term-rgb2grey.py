# -*- coding: utf-8 -*-
"""
Created on Thu Apr 25 15:55:24 2019

@author: anktkyo
"""
import matplotlib.pyplot as plt
import os
from PIL import Image
import numpy as np
import math

#将彩色图转换为灰度图
def rgb2gray(rgb):
    a=np.dot(rgb[...,:3], [299/1000, 587/1000, 114/1000])
    a.astype(np.int)
    return a


if __name__ == '__main__':
    imgpath='./histogram_images/'           #图片来源到的文件夹路径
    newpath='./histogram_samesize/'
    imagelist=os.listdir(imgpath)         #获取图像名称列表
    total=len(imagelist)

    for item in imagelist:
        path=imgpath+item
        pathnew=newpath+item
        img=Image.open(path,'r')
        print(img.mode)
        if img.mode=='P':
            img=img.convert('RGB')
        img500=img.resize((500,500),Image.BILINEAR)
        img500.save(pathnew,'jpeg')

    
    imgpath='./histogram_samesize/'
    newpath='./histogram_grey/'
    for item in imagelist:
        path=imgpath+item
        pathnew=newpath+item
        I = Image.open(path)
        L = I.convert('L')
        L.save(path)
 
