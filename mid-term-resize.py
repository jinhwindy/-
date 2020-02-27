# -*- coding: utf-8 -*-
"""
Created on Fri Apr 26 18:04:04 2019

@author: anktkyo
"""

import matplotlib.pyplot as plt
import numpy as np
from PIL import Image
import matplotlib
import imageio

def Nearest(greyimg,goalShape):
    originheight,originwidth=greyimg.shape
    goalheight,goalwidth=goalShape
    
    result=np.zeros((goalheight,goalwidth),dtype=np.uint8)
    
    for i in range(0,goalheight):
        for j in range(0,goalwidth):
            x=int(i*(originheight/goalheight)+0.5)
            y=int(j*(originwidth/goalwidth)+0.5)
            result[i][j]=greyimg[x-1][y-1]
    
    return result


def BiLinear(greyimg,goalShape):
    originheight,originwidth=greyimg.shape
    goalheight,goalwidth=goalShape
    
    result=np.zeros((goalheight,goalwidth),dtype=np.uint8)
    
    for i in range(0,goalheight-2):
        for j in range(0,goalwidth-2):
            x=(i+0.5)*(originheight/goalheight)-0.5
            y=(j+0.5)*(originwidth/goalwidth)-0.5
            x1=int(x)
            y1=int(y)
            x2=x1+1
            y2=y1+1
            q11=(x1,y1)
            q12=(x1,y2)
            q21=(x2,y1)
            q22=(x2,y2)
            
            #在x方向线性插值
            fr1=(x2-x)*greyimg[q11[0],q11[1]]+(x-x1)*greyimg[q21[0],q21[1]]
            fr2=(x2-x)*greyimg[q12[0],q12[1]]+(x-x1)*greyimg[q22[0],q22[1]]
            #在y方向线性插值
            fp=(y2-y)*fr1+(y-y1)*fr2
            result[i][j]=fp
            
    return result
            
def BiCubic_math(x,a):
    xabs=np.abs(x)
    if xabs<=1:
        return (a+2)*(xabs**3)-(a+3)*(xabs**2)+1
    elif xabs<2:
        return a*(xabs**3)-5*a*(xabs**2)+8*a*xabs-4*a
    else:
        return 0
    
def BiCubic(greyimg,goalShape):
    originheight,originwidth=greyimg.shape
    goalheight,goalwidth=goalShape
    
    result=np.zeros((goalheight,goalwidth),dtype=np.uint8)
    for i in range(0,goalheight):
        for j in range(0,goalwidth):
            x=(i+0.5)*(originheight/goalheight)-0.5
            y=(j+0.5)*(originwidth/goalwidth)-0.5
            xi=int(x)
            yi=int(y)
            u=x-xi
            v=y-yi
            wu=[0,0,0,0]
            wv=[0,0,0,0]
            tmp=0
            if (xi-1)>=0 and (xi+2)<originheight and(yi-1)>=0 and(yi+2)<originwidth:
                for ki in range(-2,2):
                    wu[ki]=(BiCubic_math(u+ki,-1))
                    wv[ki]=(BiCubic_math(v+ki,-1))
                for ki in range(-2,2):
                    for kj in range(-2,2):
                        wi=wu[ki]*wv[kj]
                        tmp+=greyimg[xi-ki,yi-kj]*wi
                result[i][j]=tmp
    return result
    
    

if __name__=='__main__':
    
    imgpath="./histogram_samesize/0h.jpg"  #原始图片的文件夹
    
    img = Image.open(imgpath).convert("L")
    img = np.array(img)


    imgnearest=Nearest(img,(1500,1500))
    imageio.imwrite('./0ha.jpg',imgnearest)
    
    imgbilinear=BiLinear(img,(1500,1500))
    imageio.imwrite('./0hb.jpg',imgbilinear)

    imgbicubic=BiCubic(img,(1500,1500))
    imageio.imwrite('./0hc.jpg',imgbicubic)