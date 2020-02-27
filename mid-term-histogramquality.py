# -*- coding: utf-8 -*-
"""
Created on Thu Apr 25 16:53:51 2019

@author: anktkyo
"""
import matplotlib.pyplot as plt
import numpy as np
from PIL import Image
import matplotlib
import os

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

#进行直方图均衡，his为上面的归一化直方图
def histogramtoequal(greyimage,hist,greylevels):
    histsum=hist.copy()
    sumtmp=0.0
    #计算累计的概率
    for i in range(greylevels):
        sumtmp=sumtmp+hist[i]
        histsum[i]=sumtmp*(greylevels-1)
        
    width,height=greyimage.shape
    result=np.zeros((width,height),dtype=np.uint8)
    
    #对每一个像素重新计算灰度级别
    for i in range(width):
        for j in range(height):
            result[i][j]=int(histsum[greyimage[i][j]]+0.5)
            #+0.5是为了四舍五入
    return result

def drawhistogram(equalhist,histtype):
    keylist=equalhist.keys()
    valuelist=equalhist.values()
    #判断直方图类型
    if histtype != None:
        plt.title(histtype)
    plt.bar(tuple(keylist),tuple(valuelist))#绘制直方图
    
    

if __name__ == '__main__':
#解决图片中中文无法正常显示的问题
    matplotlib.rcParams['font.sans-serif']=['SimHei']   # 用黑体显示中文
    plt.rcParams['axes.unicode_minus'] = False

    originpath="./histogram_samesize/"  #原始图片的文件夹
    savepath="./histogram_result/"    #保存图片的文件夹
    imagelist=os.listdir(originpath)         #获取图像名称列表
    total=len(imagelist)
    for item in imagelist: 
        imgpath = originpath+item  #原始图片的路径
        saveimgpath=savepath+item
        #imgpath = "./histogram_samesize/69h.jpg"  #原始图片的路径
        #savepath="./histogram_result/69h.jpg"
        
       
        if os.path.exists(saveimgpath):
            print("Already Exist")
            continue
        
        #打开文件
        img = Image.open(imgpath).convert("L")
        img = np.array(img)

        #绘制原始图像
        plt.figure(figsize=(10,10))   #figsize设置为图像大小
        plt.subplot(2,2,1)
        plt.imshow(img,cmap = 'gray')
        plt.title("原始灰度图")

        #创建原始直方图
        plt.subplot(2,2,3)
        historigin = greytohistogram(img,256)
        drawhistogram(historigin,"原始直方图")
        
        #计算均衡化的新的图片
        imgresult = histogramtoequal(img,historigin,256)
        plt.subplot(2,2,2)
        plt.imshow(imgresult,cmap="gray")
        plt.title("均衡的灰度图")
        
        #根据新的图片的数组，计算新的直方图
        plt.subplot(2,2,4)
        histresult = greytohistogram(imgresult,256)
        drawhistogram(histresult,"均衡直方图")
        #整理布局
        plt.tight_layout()
        #保存绘制的figure
        plt.savefig(saveimgpath[0:-4]+'bmp.jpg')
        plt.show()
        plt.close()

    
    
    
    
    
    
    
    
    
    