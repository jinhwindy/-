
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
                histogram[greyimage[i][j]]=0
            else:
                histogram[greyimage[i][j]]=histogram[greyimage[i][j]]+1
    
    #对直方图数据归一化，即计算概率
    n=width*height
    for k in histogram.keys():
        histogram[k]=histogram[k]*1.0/n
        
    return histogram


def histogrammatch(greyimg,goalhist,greylevels):

    #统计目标直方图的累计分布
    sumtmp=0.0
    goalhistsum=goalhist.copy()  #得到随机变量z，即目标直方图
    for i in range(greylevels):
        sumtmp=sumtmp+goalhist[i]
        goalhistsum[i]=sumtmp*(greylevels-1)
    #整数化
    goalhistint=[]
    for i in range(greylevels):
        goalhistint.append(int(goalhistsum[i]+0.5))
    
    #统计原图像的累计分布
    imghist=greytohistogram(greyimg,greylevels)  #得到随机变量s，即图片的直方图
    histsum=imghist.copy()
    sumtmp=0.0
    #计算累计的概率
    for i in range(greylevels):
        sumtmp=sumtmp+imghist[i]
        histsum[i]=sumtmp*(greylevels-1)
    #整数化
    histint=[]
    for i in range(greylevels):
        histint.append(int(histsum[i]+0.5))
        
    #计算从z到s的映射
    s2z=np.zeros(greylevels)
    for i in range(greylevels):
        minscale=256
        index=0
        aim=histint[i]
        for j in range(0,len(goalhistint)):
            if np.fabs(aim-goalhistint[j])<minscale:
                minscale=np.fabs(aim-goalhistint[j])
                index=j
        s2z[i]=index
    
    width,height=greyimg.shape
    result=np.zeros((width,height),dtype=np.uint8)
    
    #对每一个像素重新计算灰度级别
    for i in range(width):
        for j in range(height):
            result[i][j]=s2z[greyimg[i][j]]
    return result


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
    
    originpath="./histogram_samesize/"  #原始图片的文件夹
    savepath="./histogram_match/"    #保存图片的文件夹
    img_match = "./histogram_samesize/54h.jpg"
    imagelist=os.listdir(originpath)         #获取图像名称列表
    total=len(imagelist)
    
    
    for item in imagelist: 
        imgpath = originpath+item  #原始图片的路径
        saveimgpath=savepath+item
        #imgpath = "./histogram_samesize/50h.jpg"  #原始图片的路径
        #saveimgpath="./histogram_match/50h.jpg"
        #打开图片
        img = Image.open(imgpath).convert("L")
        img = np.array(img)
        #a=min_max(img)
        #打开指定图片
        imgmatch = Image.open(img_match).convert("L")
        imgmatch = np.array(imgmatch)
        """
        for i in range(0,img.shape[0]):
            for j in range(0,img.shape[1]):
                img[i][j]=100
        img[0][1]=5
        """
        if os.path.exists(saveimgpath):
            print("Already Exist")
            continue
        
        #开始绘图
        plt.figure(figsize=(15,10))
        #原始图和直方图
        plt.subplot(2,3,1)
        plt.title("原始图片")
        plt.imshow(img,cmap='gray')
    
        plt.subplot(2,3,4)
        originhist = greytohistogram(img,256)
        drawhistogram(originhist,"原始直方图")
    
        #match图和其直方图
        plt.subplot(2,3,2)
        plt.title("match图片")
        plt.imshow(imgmatch,cmap='gray')
        
        plt.subplot(2,3,5)
        matchhist = greytohistogram(imgmatch,256)
        drawhistogram(matchhist,"match直方图")
    
        #match后的图片及其直方图
        imgresult = histogrammatch(img,matchhist,256)#将目标图的直方图用于给原图做均衡，也就实现了match
        plt.subplot(2,3,3)
        plt.title("match后的图片")
        plt.imshow(imgresult,cmap='gray')
    
        plt.subplot(2,3,6)
        histresult = greytohistogram(imgresult,256)
        drawhistogram(histresult,"match后的直方图")
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
