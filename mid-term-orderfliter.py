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

#生成椒盐噪声
def saltNoise(greyimg,noiseNum):
    result=greyimg.copy()
    height,width=greyimg.shape
    
    for i in range(0,noiseNum):
        noisex=random.randint(0,height-1)
        noisey=random.randint(0,width-1)
        salt=random.randint(0,2)
        if salt==0:
            result[noisex][noisey]=0
        else:
            result[noisex][noisey]=255
    return result

#生成高斯噪声
def gaussNoise(greyimg,noiseNum,means,sigma):
    result=greyimg.copy()
    height,width=greyimg.shape
    
    for i in range(0,noiseNum):
        noisex=random.randint(0,height-1)
        noisey=random.randint(0,width-1)
        result[noisex][noisey]+=random.gauss(means,sigma)
        if result[noisex][noisey]<0:
            result[noisex][noisey]=0
        elif result[noisex][noisey]>255:
            result[noisex][noisey]=255
    
    return result
    
#均值滤波器
def orderFliter(greyimg,windowsize,typename):
    addborder=int(windowsize*1.0/2)  #加边宽度
    #采用边界颜色填充
    newimg=cv2.copyMakeBorder(greyimg,addborder,addborder,addborder,addborder,cv2.BORDER_REPLICATE)
    result=greyimg.copy()    
    height,width=newimg.shape
    
    #均值滤波窗口开始移动
    for i in range(addborder,height-addborder):
        for j in range(addborder,width-addborder):
            mask=newimg[i-addborder:i+addborder+1,j-addborder:j+addborder+1]
            
            if typename=='最小值':
                value=np.min(mask)
            elif typename=='中值':
                value=np.median(mask)
            elif typename=='最大值':
                value=np.max(mask)
                
            result[i-addborder][j-addborder]=value
            
    return result
    


if __name__=='__main__':
    matplotlib.rcParams['font.sans-serif']=['SimHei']   # 用黑体显示中文
    plt.rcParams['axes.unicode_minus'] = False

    originpath="./histogram_reducedsamesize/"  #原始图片的文件夹
    savepath="./orderfliter/"    #保存图片的文件夹
    imagelist=os.listdir(originpath)         #获取图像名称列表
    total=len(imagelist)
    count=0
    #imgpath="./histogram_samesize/0h.jpg"  #原始图片的文件夹
    for item in imagelist:
        """
        if count>1:
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
      
    
        plt.figure(figsize=(20,12))
        
        plt.subplot(3,6,1)
        plt.imshow(img,cmap = 'gray')
        plt.title("原始灰度图")  
        
        imgsalt=saltNoise(img,2000)  #两千个噪声点
        plt.subplot(3,6,7)
        plt.imshow(imgsalt,cmap = 'gray')
        plt.title("加椒盐噪声灰度图")     
    
        imggauss=gaussNoise(img,2000,0,100)    
        plt.subplot(3,6,13)
        plt.imshow(imggauss,cmap = 'gray')
        plt.title("加椒盐噪声灰度图")  
        
        img_meanf=orderFliter(img,3,'中值')
        plt.subplot(3,6,2)
        plt.imshow(img_meanf,cmap = 'gray')
        plt.title("原始灰度图中值滤波-3")      
        
        imgsalt_meanf=orderFliter(imgsalt,3,'中值')
        plt.subplot(3,6,8)
        plt.imshow(imgsalt_meanf,cmap = 'gray')
        plt.title("加椒盐噪声中值滤波-3")      
        
        imggauss_meanf=orderFliter(imggauss,3,'中值')
        plt.subplot(3,6,14)
        plt.imshow(imggauss_meanf,cmap = 'gray')
        plt.title("高斯噪声中值滤波-3")        
        
        img_meanf=orderFliter(img,9,'中值')
        plt.subplot(3,6,3)
        plt.imshow(img_meanf,cmap = 'gray')
        plt.title("原始灰度图中值滤波-9")      
        
        imgsalt_meanf=orderFliter(imgsalt,9,'中值')
        plt.subplot(3,6,9)
        plt.imshow(imgsalt_meanf,cmap = 'gray')
        plt.title("加椒盐噪声中值滤波-9")      
        
        imggauss_meanf=orderFliter(imggauss,9,'中值')
        plt.subplot(3,6,15)
        plt.imshow(imggauss_meanf,cmap = 'gray')
        plt.title("高斯噪声中值滤波-9")        
        
        img_meanf=orderFliter(img,17,'中值')
        plt.subplot(3,6,4)
        plt.imshow(img_meanf,cmap = 'gray')
        plt.title("原始灰度图中值滤波-17")      
        
        imgsalt_meanf=orderFliter(imgsalt,17,'中值')
        plt.subplot(3,6,10)
        plt.imshow(imgsalt_meanf,cmap = 'gray')
        plt.title("加椒盐噪声中值滤波-17")      
        
        imggauss_meanf=orderFliter(imggauss,17,'中值')
        plt.subplot(3,6,16)
        plt.imshow(imggauss_meanf,cmap = 'gray')
        plt.title("高斯噪声中值滤波-17")     
        
        img_meanf=orderFliter(img,3,'最大值')
        plt.subplot(3,6,5)
        plt.imshow(img_meanf,cmap = 'gray')
        plt.title("原始灰度图最大值滤波-3")      
        
        imgsalt_meanf=orderFliter(imgsalt,3,'最大值')
        plt.subplot(3,6,11)
        plt.imshow(imgsalt_meanf,cmap = 'gray')
        plt.title("加椒盐噪声最大值滤波-3")      
        
        imggauss_meanf=orderFliter(imggauss,3,'最大值')
        plt.subplot(3,6,17)
        plt.imshow(imggauss_meanf,cmap = 'gray')
        plt.title("高斯噪声最大值滤波-3")   
        
        img_meanf=orderFliter(img,3,'最小值')
        plt.subplot(3,6,6)
        plt.imshow(img_meanf,cmap = 'gray')
        plt.title("原始灰度图最小值滤波-3")      
        
        imgsalt_meanf=orderFliter(imgsalt,3,'最小值')
        plt.subplot(3,6,12)
        plt.imshow(imgsalt_meanf,cmap = 'gray')
        plt.title("加椒盐噪声最小值滤波-3")      
        
        imggauss_meanf=orderFliter(imggauss,3,'最小值')
        plt.subplot(3,6,18)
        plt.imshow(imggauss_meanf,cmap = 'gray')
        plt.title("高斯噪声最小值滤波-3")           
        #整理布局
        plt.tight_layout() 
        plt.savefig(saveimgpath[0:-4]+'.jpg')
        #plt.savefig('./a.jpg')
        plt.show()
        plt.close()    

    
    