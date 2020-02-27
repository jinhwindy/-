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


    

def laplacianFliter(greyimg,typeclass,typename):
    windowsize=3
    addborder=int(windowsize*1.0/2)  #加边宽度
    #采用边界颜色填充
    newimg=cv2.copyMakeBorder(greyimg,addborder,addborder,addborder,addborder,cv2.BORDER_REPLICATE)
    result=greyimg.copy()  
    result=np.int16(result)
    if typeclass=='h1':
        window=np.array([[0,-1,0],[-1,4,-1],[0,-1,0]],dtype=np.int8)
    elif typeclass=='h2':
        window=np.array([[-1,-1,-1],[-1,8,-1],[-1,-1,-1]],dtype=np.int8)        
    elif typeclass=='h3':
        window=np.array([[1,-2,1],[-2,4,-2],[1,-2,1]],dtype=np.int8)       
    elif typeclass=='h4':
        window=np.array([[0,-1,0],[-1,5,-1],[0,-1,0]],dtype=np.int8)       
        
    height,width=newimg.shape
    
    #均值滤波窗口开始移动
    for i in range(addborder,height-addborder):
        for j in range(addborder,width-addborder):
            mask=newimg[i-addborder:i+addborder+1,j-addborder:j+addborder+1]
            value=np.sum(mask*window)
            result[i-addborder][j-addborder]=value
    
    if typename=='取反':
        result=np.uint8(result)
        result=255-result    
    return result



if __name__=='__main__':
    matplotlib.rcParams['font.sans-serif']=['SimHei']   # 用黑体显示中文
    plt.rcParams['axes.unicode_minus'] = False

    originpath="./histogram_reducedsamesize/"  #原始图片的文件夹
    savepath="./so_fliter/"    #保存图片的文件夹
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
      
    
        plt.figure(figsize=(14,10))
        
        plt.subplot(2,3,1)
        plt.imshow(img,cmap = 'gray')
        plt.title("原始灰度图")  
        

        plt.subplot(2,3,2)
        imgh1=laplacianFliter(img,'h1','正常')
        plt.imshow(imgh1,cmap = 'gray')
        plt.title("Laplacian算子h1-正常")  

       
        plt.subplot(2,3,3)
        imgh2=laplacianFliter(img,'h2','正常')
        plt.imshow(imgh2,cmap = 'gray')
        plt.title("Laplacian算子h2-正常")  

        plt.subplot(2,3,5)
        imgh3=laplacianFliter(img,'h3','正常')
        plt.imshow(imgh3,cmap = 'gray')
        plt.title("Laplacian算子h3-正常")  

        plt.subplot(2,3,6)
        imgh4=laplacianFliter(img,'h4','正常')
        plt.imshow(imgh4,cmap = 'gray')
        plt.title("Laplacian算子h4-正常")         
         

        #整理布局
        plt.tight_layout() 
        plt.savefig(saveimgpath[0:-4]+'.jpg')
        #plt.savefig('./a.jpg')
        plt.show()
        #plt.close()    
