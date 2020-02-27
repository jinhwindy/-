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

    

def horizontalFliter(greyimg,typename):
    windowsize=3
    addborder=int(windowsize*1.0/2)  #加边宽度
    #采用边界颜色填充
    newimg=cv2.copyMakeBorder(greyimg,addborder,addborder,addborder,addborder,cv2.BORDER_REPLICATE)
    result=greyimg.copy()  
    result=np.int16(result)
    window=np.array([[1,2,1],[0,0,0],[-1,-2,-1]],dtype=np.int16)
    height,width=newimg.shape
    
    #均值滤波窗口开始移动
    for i in range(addborder,height-addborder):
        for j in range(addborder,width-addborder):
            mask=newimg[i-addborder:i+addborder+1,j-addborder:j+addborder+1]
            mean=np.sum(mask*window)     
            result[i-addborder][j-addborder]=mean
            
    if typename=='加值':
        minv=np.min(result)
        if minv<0:
            result=result+np.abs(minv)
    elif typename=='绝对值':
        result=np.abs(result)
    elif typename=='绝对值取反':
        result=np.abs(result)
        result=np.uint8(result)
        result=255-result        
    return result
    

def verticalFliter(greyimg,typename):
    windowsize=3
    addborder=int(windowsize*1.0/2)  #加边宽度
    #采用边界颜色填充
    newimg=cv2.copyMakeBorder(greyimg,addborder,addborder,addborder,addborder,cv2.BORDER_REPLICATE)
    result=greyimg.copy()  
    result=np.int16(result)
    window=np.array([[1,0,-1],[2,0,-2],[1,0,-1]],dtype=np.int16)
    height,width=newimg.shape
    
    #均值滤波窗口开始移动
    for i in range(addborder,height-addborder):
        for j in range(addborder,width-addborder):
            mask=newimg[i-addborder:i+addborder+1,j-addborder:j+addborder+1]
            mean=np.sum(mask*window)     
            result[i-addborder][j-addborder]=mean
            
    if typename=='加值':
        minv=np.min(result)
        if minv<0:
            result=result+np.abs(minv)
    elif typename=='绝对值':
        result=np.abs(result)
    elif typename=='绝对值取反':
        result=np.abs(result)
        result=np.uint8(result)
        result=255-result
    return result



if __name__=='__main__':
    matplotlib.rcParams['font.sans-serif']=['SimHei']   # 用黑体显示中文
    plt.rcParams['axes.unicode_minus'] = False

    originpath="./histogram_reducedsamesize/"  #原始图片的文件夹
    savepath="./singledir_fofliter/"    #保存图片的文件夹
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
      
    
        plt.figure(figsize=(15,8))
        
        plt.subplot(2,4,1)
        plt.imshow(img,cmap = 'gray')
        plt.title("原始灰度图")  
        

        plt.subplot(2,4,2)
        imghadd=horizontalFliter(img,'加值')
        plt.imshow(imghadd,cmap = 'gray')
        plt.title("水平锐化灰度图-加值")  
        
        plt.subplot(2,4,3)
        imghabs=horizontalFliter(img,'绝对值')
        imghabs=Image.fromarray(imghabs)
        plt.imshow(imghabs,cmap = 'gray')
        plt.title("水平锐化灰度图-绝对值")  

        plt.subplot(2,4,4)
        imghabsf=horizontalFliter(img,'绝对值取反')
        imghabsf=Image.fromarray(imghabsf)
        plt.imshow(imghabsf,cmap = 'gray')
        plt.title("水平锐化灰度图-绝对值取反")  

        plt.subplot(2,4,6)
        imgvadd=verticalFliter(img,'加值')

        plt.imshow(imgvadd,cmap = 'gray')
        plt.title("垂直锐化灰度图-加值")  
        
        plt.subplot(2,4,7)
        imgvabs=verticalFliter(img,'绝对值')
        imgvabs=Image.fromarray(imgvabs)
        plt.imshow(imgvabs,cmap = 'gray')
        plt.title("垂直锐化灰度图-绝对值")  

        plt.subplot(2,4,8)
        imgvabsf=verticalFliter(img,'绝对值取反')
        imgvabsf=Image.fromarray(imgvabsf)
        plt.imshow(imgvabsf,cmap = 'gray')
        plt.title("垂直锐化灰度图-绝对值取反")  
        
        #整理布局
        plt.tight_layout() 
        plt.savefig(saveimgpath[0:-4]+'.jpg')
        #plt.savefig('./a.jpg')
        plt.show()
        plt.close()    

    
    