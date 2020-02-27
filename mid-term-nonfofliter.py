# -*- coding: utf-8 -*-
"""
Created on Fri Apr 26 23:17:13 2019

@author: anktkyo
"""
import random
import matplotlib.pyplot as plt
import numpy as np
from PIL import Image
import matplotlib
import imageio
import cv2
import os

    

def robertsFliter(greyimg,typename):
    windowsize=2
    addborder=int(windowsize/2)  #加边宽度
    #采用边界颜色填充
    newimg=cv2.copyMakeBorder(greyimg,addborder,addborder,addborder,addborder,cv2.BORDER_REPLICATE)
    result=greyimg.copy()  
    result=np.int16(result)
    windowx=np.array([[1,0],[0,-1]],dtype=np.int8)
    windowy=np.array([[0,1],[-1,0]],dtype=np.int8)
    height,width=newimg.shape
    
    #均值滤波窗口开始移动
    for i in range(addborder,height-addborder):
        for j in range(addborder,width-addborder):
            mask=newimg[i:i+addborder+1,j:j+addborder+1]
            x=np.abs(np.sum(mask*windowx))
            y=np.abs(np.sum(mask*windowy))   
            result[i-addborder][j-addborder]=(x+y)
    
    if typename=='取反':
        result=np.uint8(result)
        result=255-result    
    return result
    

def sobelFliter(greyimg,typename):
    windowsize=3
    addborder=int(windowsize*1.0/2)  #加边宽度
    #采用边界颜色填充
    newimg=cv2.copyMakeBorder(greyimg,addborder,addborder,addborder,addborder,cv2.BORDER_REPLICATE)
    result=greyimg.copy()  
    result=np.int16(result)
    windowx=np.array([[-1,0,1],[-2,0,2],[-1,0,1]],dtype=np.int8)
    windowy=np.array([[-1,-2,-1],[0,0,0],[1,2,1]],dtype=np.int8)
    height,width=newimg.shape
    
    #均值滤波窗口开始移动
    for i in range(addborder,height-addborder):
        for j in range(addborder,width-addborder):
            mask=newimg[i-addborder:i+addborder+1,j-addborder:j+addborder+1]
            x=(np.sum(mask*windowx)**2)
            y=(np.sum(mask*windowy)**2)   
            result[i-addborder][j-addborder]=np.sqrt(x+y)
    
    if typename=='取反':
        result=np.uint8(result)
        result=255-result    
    return result


def priwittFliter(greyimg,typename):
    windowsize=3
    addborder=int(windowsize*1.0/2)  #加边宽度
    #采用边界颜色填充
    newimg=cv2.copyMakeBorder(greyimg,addborder,addborder,addborder,addborder,cv2.BORDER_REPLICATE)
    result=greyimg.copy()  
    result=np.int16(result)
    windowx=np.array([[-1,0,1],[-1,0,1],[-1,0,1]],dtype=np.int8)
    windowy=np.array([[-1,-1,-1],[0,0,0],[1,1,1]],dtype=np.int8)
    height,width=newimg.shape
    
    #均值滤波窗口开始移动
    for i in range(addborder,height-addborder):
        for j in range(addborder,width-addborder):
            mask=newimg[i-addborder:i+addborder+1,j-addborder:j+addborder+1]
            x=(np.sum(mask*windowx)**2)
            y=(np.sum(mask*windowy)**2)   
            result[i-addborder][j-addborder]=np.sqrt(x+y)
    
    if typename=='取反':
        result=np.uint8(result)
        result=255-result    
    return result

if __name__=='__main__':
    matplotlib.rcParams['font.sans-serif']=['SimHei']   # 用黑体显示中文
    plt.rcParams['axes.unicode_minus'] = False

    originpath="./histogram_reducedsamesize/"  #原始图片的文件夹
    savepath="./nondir_fofliter/"    #保存图片的文件夹
    imagelist=os.listdir(originpath)         #获取图像名称列表
    total=len(imagelist)
    count=0
    #imgpath="./histogram_samesize/0h.jpg"  #原始图片的文件夹
    for item in imagelist:
        """
        if count>2:
            break
        count+=1
        """
        imgpath = originpath+item  #原始图片的路径
        saveimgpath=savepath+item        
        if imgpath[-4:]=='.bmp':
            print('bmp')
            continue
        img = Image.open(imgpath).convert("L")
        img = np.array(img)
      
    
        plt.figure(figsize=(10,10))
        
        plt.subplot(3,3,1)
        plt.imshow(img,cmap = 'gray')
        plt.title("原始灰度图")  
        

        plt.subplot(3,3,2)
        imgroberts=robertsFliter(img,'正常')
        plt.imshow(imgroberts,cmap = 'gray')
        plt.title("roberts一阶锐化-正常")  
        
        plt.subplot(3,3,3)
        imgrobertsf=robertsFliter(img,'取反')
        plt.imshow(imgrobertsf,cmap = 'gray')
        plt.title("roberts一阶锐化-取反")  
        
        plt.subplot(3,3,5)
        imgsobel=sobelFliter(img,'正常')
        plt.imshow(imgsobel,cmap = 'gray')
        plt.title("sobel一阶锐化-正常")  
        
        plt.subplot(3,3,6)
        imgsobelf=sobelFliter(img,'取反')
        plt.imshow(imgsobelf,cmap = 'gray')
        plt.title("sobel一阶锐化-取反")          
        
        plt.subplot(3,3,8)
        imgpriwitt=priwittFliter(img,'正常')
        plt.imshow(imgpriwitt,cmap = 'gray')
        plt.title("priwitt一阶锐化-正常")  
        
        plt.subplot(3,3,9)
        imgpriwittf=priwittFliter(img,'取反')
        plt.imshow(imgpriwittf,cmap = 'gray')
        plt.title("priwitt一阶锐化-取反")   
        #整理布局
        plt.tight_layout() 
        plt.savefig(saveimgpath[0:-4]+'.jpg')
        #plt.savefig('./a.jpg')
        plt.show()
        plt.close()    
