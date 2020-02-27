# -*- coding: utf-8 -*-
"""
Created on Mon Apr 22 21:07:55 2019

@author: anktkyo
"""

from urllib import request
import time
import os

urlpath='./images_urls.txt'     #images_urls.txt中存储着要下载图片的urls
savepath='./images/'           #图片保存到的文件夹路径

file=open(urlpath,'r')
with open(urlpath, 'r') as fr:  # 加载文件
        txtlist = [line.strip("\n").split('\t') for line in fr.readlines()]
        namelist = [line[0] for line in txtlist]
        urllist = [line[1] for line in txtlist]



imagecount=2021

for i in range(11403,len(urllist)):
    if imagecount>2700:
        break
    try:
        imagepath=savepath+str(imagecount)+'.jpg'     #每一张图片的名称
        #request.urlretrieve(line,imagepath)
        web = request.urlopen(urllist[i],timeout=5)
        time.sleep(0.5)
        data = web.read()
        f = open(imagepath,"wb")
        f.write(data)
        f.close()
        print('%s.jpg' %namelist[i])
        imagecount=imagecount+1
    except request.HTTPError as reason:                                
        print("%d,fail to download, caused by HTTPError" %i)                
        continue                                                       
    except request.URLError as reason:                                 
        print("%d,fail to download, caused by URLError" %i)                 
        continue                                                       
    except:                                                            
        print("%d, FAILED for unknow reason!" %i)                           
        continue


file.close()