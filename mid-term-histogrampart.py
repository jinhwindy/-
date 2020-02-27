
# -*- coding: utf-8 -*-
"""
Created on Thu Apr 25 20:46:11 2019

@author: anktkyo
"""

import matplotlib.pyplot as plt
import numpy as np
from PIL import Image
import matplotlib
import os
import scipy.misc

def min_max(greyimage):
    width,height=greyimage.shape
    result=np.zeros((width,height))
    minv=np.min(greyimage)
    maxv=np.max(greyimage)
    """
    for i in range(width):
        for j in range(height):
            if greyimage[i][j]>maxv:
                maxv=greyimage[i][j]
            if greyimage[i][j]<minv:
                minv=greyimage[i][j]
                """
    
    for i in range(width):
        for j in range(height):
            result[i][j]=(greyimage[i][j]-0)*1.0/(255)
    return result


#将图像数据转化为相应的归一化直方图
def greytohistogram(greyimage,greylevels):
    width,height=greyimage.shape
    histogram={}
    #初始化直方图数据
    for i in range(greylevels):
        histogram[i]=0
    #统计直方图数据
    for i in range(width):
        for j in range(height):
            if histogram.get(greyimage[i][j]) is None:
                histogram[greyimage[i][j]]=0;
            else:
                histogram[greyimage[i][j]]=histogram[greyimage[i][j]]+1
    
    #对直方图数据归一化，即计算概率
    n=width*height
    for k in histogram.keys():
        histogram[k]=histogram[k]*1.0/n
        
    return histogram


def histogrampart(greyimg,windowsize,greylevels,k0,k1,k2,E):
    height,width=greyimg.shape
    count=greytohistogram(greyimg,greylevels) #计算得到count直方图分布
    globalmean=0.0
    #计算全局均值
    for i in range(0,greylevels):
        globalmean+=(i*count[i])
    globalvariance=0.0
    #计算全局方差
    for i in range(0,greylevels):
        globalvariance+=((i-globalmean)**2)*count[i]
    globalvariance=np.sqrt(globalvariance)    
    localmean=0.0
    localvariance=0.0
    localn=windowsize*windowsize  #模版大小
    result=np.zeros((height,width),dtype=np.uint8)
    for i in range(int(windowsize/2),height-int(windowsize/2)-1):
        for j in range(int(windowsize/2),width-int(windowsize/2)-1):
            localcount={}
            localmean=0.0
            localvariance=0.0
            #初始化直方图数据
            for k in range(greylevels):
                localcount[k]=0
            #统计局部直方图信息，存与localcount中
            for kj in range(j-int(windowsize/2),j+int(windowsize/2)+1):
                for ki in range(i-int(windowsize/2),i+int(windowsize/2)+1):
                    if localcount.get(greyimg[ki][kj]) is None:
                        localcount[greyimg[ki][kj]]=0
                    else:
                        localcount[greyimg[ki][kj]]+=(1.0/localn)
            #计算局部均值
            for k in range(0,greylevels):
                localmean+=(k*localcount[k])
            #计算局部方差
            for k in range(0,greylevels):
                localvariance+=((k-localmean)**2)*localcount[k]
            localvariance=np.sqrt(localvariance)        
            #判断是否进行增强

            if localmean<=k0*globalmean and localvariance>=k1*globalvariance and localvariance<=k2*globalvariance:
                result[i][j]=int(E*greyimg[i][j])
            else:
                result[i][j]=greyimg[i][j]

            
    return result,globalmean,globalvariance


def drawhistogram(equalhist,histtype):
    keylist=equalhist.keys()
    valuelist=equalhist.values()
    #判断直方图类型
    if histtype != None:
        plt.title(histtype)
    plt.bar(tuple(keylist),tuple(valuelist))#绘制直方图
    


if __name__ == '__main__':
    matplotlib.rcParams['font.sans-serif']=['SimHei']   # 用黑体显示中文
    plt.rcParams['axes.unicode_minus'] = False
    
    originpath="./histogram_reducedsamesize/"  #原始图片的文件夹
    savepath="./histogram_part/"    #保存图片的文件夹
    imagelist=os.listdir(originpath)         #获取图像名称列表
    total=len(imagelist)
    c=0
    
    for item in imagelist: 
        imgpath = originpath+item  #原始图片的路径
        saveimgpath=savepath+item
        #imgpath = "./histogram_samesize/50h.jpg"  #原始图片的路径
        #saveimgpath="./histogram_match/50h.jpg"
        #打开图片
        if imgpath[-4:]=='.bmp':
            print('bmp')
            continue
        """
        if c>0:
            break
        c+=1
        """
        img = Image.open(imgpath).convert("L")
        img=np.asarray(img)
        img= Image.fromarray(img)

        
        #开始绘图
        plt.figure(figsize=(15,10))
        #原始图和直方图
        plt.subplot(2,3,1)
        plt.title("原始图片")
        plt.imshow(img,cmap='gray')
        img=np.asarray(img)
        plt.subplot(2,3,4)
        originhist = greytohistogram(img,256)
        drawhistogram(originhist,"原始直方图")

        #match图和其直方图
        img=np.asarray(img)
        imgpart,gmean,gvar=histogrampart(img,3,256,0.4,0.02,0.4,4.0)
        plt.subplot(2,3,2)
        plt.title("k0=0.4;k1=0.02;k2=0.4;E=4.0")
        plt.imshow(imgpart,cmap='gray')
        
        plt.subplot(2,3,5)
        parthist = greytohistogram(imgpart,256)
        drawhistogram(parthist,"直方图")

        #match图和其直方图
        img=np.asarray(img)
        imgpart1,gmean,gvar=histogrampart(img,3,256,0.4,0.008,0.2,5.0)
        plt.subplot(2,3,3)
        plt.title("k0=0.4;k1=0.008;k2=0.2;E=5.0")
        plt.imshow(imgpart1,cmap='gray')
        
        plt.subplot(2,3,6)
        parthist1 = greytohistogram(imgpart1,256)
        drawhistogram(parthist1,"直方图")


        #整理布局
        plt.tight_layout()
        #保存绘制的figure
        if imgpath[-4:]=='.jpg':
            savea=saveimgpath
        else :
            if imgpath[-4:]=='.bmp':
                savea=saveimgpath[0:-4]+'bmp.jpg'
        plt.savefig(savea)

        plt.show()
        plt.close()
