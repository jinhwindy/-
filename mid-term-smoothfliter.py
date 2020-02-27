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
def meanFliter(greyimg,windowsize):
    addborder=int(windowsize*1.0/2)  #加边宽度
    #采用边界颜色填充
    newimg=cv2.copyMakeBorder(greyimg,addborder,addborder,addborder,addborder,cv2.BORDER_REPLICATE)
    result=greyimg.copy()    
    window=(1.0/(windowsize**2))*np.ones((windowsize, windowsize))  # 定义窗口
    height,width=newimg.shape
    
    #均值滤波窗口开始移动
    for i in range(addborder,height-addborder):
        for j in range(addborder,width-addborder):
            mask=newimg[i-addborder:i+addborder+1,j-addborder:j+addborder+1]
            """
            mean=0.0
            for ki in range(0,windowsize):
                for kj in range(0,windowsize):
                    mean+=(window[ki][kj]*mask[ki][kj])
            """
            mean=np.sum(mask*window)
            result[i-addborder][j-addborder]=int(mean+0.5)
            
    return result
    


if __name__=='__main__':
    matplotlib.rcParams['font.sans-serif']=['SimHei']   # 用黑体显示中文
    plt.rcParams['axes.unicode_minus'] = False

    originpath="./histogram_reducedsamesize/"  #原始图片的文件夹
    savepath="./singledirectionfliter/"    #保存图片的文件夹
    imagelist=os.listdir(originpath)         #获取图像名称列表
    total=len(imagelist)

    #imgpath="./histogram_samesize/0h.jpg"  #原始图片的文件夹
    for item in imagelist:
        imgpath = originpath+item  #原始图片的路径
        saveimgpath=savepath+item        
        if imgpath[-4:]=='.bmp':
            print('bmp')
            continue
        img = Image.open(imgpath).convert("L")
        img = np.array(img)
      
    
        plt.figure(figsize=(15,12))
        
        plt.subplot(3,4,1)
        plt.imshow(img,cmap = 'gray')
        plt.title("原始灰度图")  
        
        imgsalt=saltNoise(img,2000)  #两千个噪声点
        plt.subplot(3,4,5)
        plt.imshow(imgsalt,cmap = 'gray')
        plt.title("加椒盐噪声灰度图")     
    
        imggauss=gaussNoise(img,2000,0,100)    
        plt.subplot(3,4,9)
        plt.imshow(imggauss,cmap = 'gray')
        plt.title("加椒盐噪声灰度图")  
        
        img_meanf=meanFliter(img,3)
        plt.subplot(3,4,2)
        plt.imshow(img_meanf,cmap = 'gray')
        plt.title("原始灰度图均值滤波-3")      
        
        imgsalt_meanf=meanFliter(imgsalt,3)
        plt.subplot(3,4,6)
        plt.imshow(imgsalt_meanf,cmap = 'gray')
        plt.title("加椒盐噪声均值滤波-3")      
        
        imggauss_meanf=meanFliter(imggauss,3)
        plt.subplot(3,4,10)
        plt.imshow(imggauss_meanf,cmap = 'gray')
        plt.title("高斯噪声均值滤波-3")        
        
        img_meanf=meanFliter(img,9)
        plt.subplot(3,4,3)
        plt.imshow(img_meanf,cmap = 'gray')
        plt.title("原始灰度图均值滤波-9")      
        
        imgsalt_meanf=meanFliter(imgsalt,9)
        plt.subplot(3,4,7)
        plt.imshow(imgsalt_meanf,cmap = 'gray')
        plt.title("加椒盐噪声均值滤波-9")      
        
        imggauss_meanf=meanFliter(imggauss,9)
        plt.subplot(3,4,11)
        plt.imshow(imggauss_meanf,cmap = 'gray')
        plt.title("高斯噪声均值滤波-9")        
        
        img_meanf=meanFliter(img,17)
        plt.subplot(3,4,4)
        plt.imshow(img_meanf,cmap = 'gray')
        plt.title("原始灰度图均值滤波-17")      
        
        imgsalt_meanf=meanFliter(imgsalt,17)
        plt.subplot(3,4,8)
        plt.imshow(imgsalt_meanf,cmap = 'gray')
        plt.title("加椒盐噪声均值滤波-17")      
        
        imggauss_meanf=meanFliter(imggauss,17)
        plt.subplot(3,4,12)
        plt.imshow(imggauss_meanf,cmap = 'gray')
        plt.title("高斯噪声均值滤波-17")         
        
        #整理布局
        #plt.tight_layout() 
        plt.savefig(saveimgpath[0:-4]+'.jpg')
        #plt.savefig('./a.jpg')
        plt.show()
        plt.close()    

    
    