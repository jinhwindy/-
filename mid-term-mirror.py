# -*- coding: utf-8 -*-
"""
Created on Fri Apr 26 17:01:36 2019

@author: anktkyo
"""

import matplotlib.pyplot as plt
import numpy as np
from PIL import Image
import matplotlib
import os

def mirror(greyimg,mirrortype):
    width,height=greyimg.shape
    result=np.zeros((width,height),dtype=np.uint8)
    
    
    for i in range(0,height):
        for j in range(0,width):
            if mirrortype=='水平对称':
                result[i][j]=greyimg[i][(-1)*j+width-1]
            else:
                if mirrortype=='垂直对称':
                    result[i][j]=greyimg[(-1)*i+height-1][j]
                    
    return result

if __name__=='__main__':
    matplotlib.rcParams['font.sans-serif']=['SimHei']   # 用黑体显示中文
    plt.rcParams['axes.unicode_minus'] = False
    
    originpath="./histogram_samesize/"  #原始图片的文件夹
    savepath="./dotop_mirror/"    #保存图片的文件夹    
    imagelist=os.listdir(originpath)         #获取图像名称列表
    total=len(imagelist)
    
    for item in imagelist:
        imgpath = originpath+item  #原始图片的路径
        saveimgpath=savepath+item
        #imgpath = "./histogram_samesize/12h.jpg"  #原始图片的路径
        #saveimgpath="./dotop_mirror/12h.jpg"
        #打开图片
        img = Image.open(imgpath).convert("L")
        img = np.array(img)
        """
        if os.path.exists(saveimgpath):
            print("Already Exist")
            continue
           """ 
        #开始绘图
        plt.figure(figsize=(10,10))
        #原始图
        plt.subplot(2,2,1)
        plt.title("原始图片")
        plt.imshow(img,cmap='gray')
        
        plt.subplot(2,2,3)
        horizontal = mirror(img,'水平对称')
        plt.title("水平对称图片")
        plt.imshow(horizontal,cmap='gray')
        
        plt.subplot(2,2,4)
        vertical = mirror(img,'垂直对称')
        plt.title("垂直对称图片")
        plt.imshow(vertical,cmap='gray')
        
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