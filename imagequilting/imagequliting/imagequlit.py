# -*- coding: utf-8 -*-
import cv2 as cv
import numpy as np
import random as ran
from minpath import getMinPath
im=None
sample_size=None
imglist=None
overlap_size=None
l_img=None


def print_grid(grid):
    for row in grid:
        for e in row:
            print '\t',sum(e),
        print

#获得灰度图片
def rgb2gray(rgb):
    return np.dot(rgb[...,:4], [0.299, 0.587, 0.144, 0])

def createImageList(imglist):
    global im,sample_size
    for i in range(len(im)-sample_size):
        for j in range(len(im[0])-sample_size):
            imglist.append(im[i:i+sample_size, j:j+sample_size])


#从样例图片中创建随机图片
def createRandImage():
    global imglist
    r=ran.randint(0,len(imglist) - 1)
    return imglist[r]

#计算的2个图像垂直重叠区域之间的SSD
def computeVerticalSSD(pre_img, randimg, overlap_size):
    overlap1 = np.array(pre_img[0:len(pre_img), len(pre_img[0])-overlap_size:len(pre_img[0])], dtype=np.float64)
    overlap2 = np.array(randimg[0:len(randimg), 0:overlap_size], dtype=np.float64)

    ssd = np.sum((overlap1-overlap2)**2)
    ssd2 = np.sum((rgb2gray(overlap1)**2+rgb2gray(overlap2)**2)**0.5)
    ssd3 = np.sum(((rgb2gray(overlap1)-rgb2gray(overlap2))**2)**0.5)

    return ssd3

#计算的2个图像水平重叠区域之间的SSD
def computeHorizontalSSD(top_img, randimg, overlap_size):
    overlap1 = np.array(top_img[len(top_img)-overlap_size:len(top_img), 0:len(top_img[0])], dtype=np.float64)
    overlap2 = np.array(randimg[0:overlap_size, 0:len(top_img[0])], dtype=np.float64)

    ssd = np.sum((overlap1-overlap2)**2)
    ssd2 = np.sum((rgb2gray(overlap1)**2+rgb2gray(overlap2)**2)**0.5)
    ssd3 = np.sum(((rgb2gray(overlap1)-rgb2gray(overlap2))**2)**0.5)

    return ssd3

#计算的2个图像垂直水平重叠区域之间的SSD
def computeSSD(pre_img, top_img, randimg, overlap_size):

    if pre_img is None and top_img is None:

        return 0
    if pre_img is None:

        return computeHorizontalSSD(top_img, randimg, overlap_size)
    if top_img is None:

        return computeVerticalSSD(pre_img, randimg, overlap_size)

    return computeVerticalSSD(pre_img, randimg, overlap_size) + computeHorizontalSSD(top_img, randimg, overlap_size)

#从随机列表中返回具有最小SSD误差的图像
def getminSSDImg(pre_img, top_img):
    minSSDImg = []
    global imglist
    minSSD = 0
    minidx = 0
    for i in range(len(imglist)):
        if i==0:
            minSSD = computeSSD(pre_img, top_img, imglist[i],overlap_size)
            minSSDImg=imglist[i]
            minidx = i
        else:
            if not (np.array_equal(pre_img,imglist[i]) or np.array_equal(top_img,imglist[i])):
                ssd = computeSSD(pre_img, top_img, imglist[i],overlap_size)

                if minSSD > ssd:
                    minSSD = ssd
                    minSSDImg = imglist[i]
                    minidx = i;

    return minSSDImg

def getMin2(v1, v2):
    if v1 < v2:
        return v1
    else:
        return v2

def getMin3(v1, v2, v3):
    if v1 < v2:
        if v1 < v3:
            return v1
        else:
            return v3
    else:
        if v2 < v3:
            return v2
        else:
            return v3


#计算的最小误差边界
def compVertMinErrBoun(pre_img, cur_img, overlap_size):
    overlap1 = np.array(pre_img[0:len(pre_img), len(pre_img[0])-overlap_size:len(pre_img[0])], dtype=np.float64)
    overlap2 = np.array(cur_img[0:len(cur_img), 0:overlap_size], dtype=np.float64)
    error = ((rgb2gray(overlap1)-rgb2gray(overlap2))**2)**0.5
    
    
    path = getMinPath(error)
    print pre_img.shape, cur_img.shape

    for i in path:

        for k in range(i[1]):
            cur_img[i[0]][k]=overlap1[i[0]][k]
    

    
def compHorMinErrBoun(top_img, cur_img, overlap_size):
    imgT=np.transpose(top_img, axes=(1, 0, 2))
    randimgT=np.transpose(cur_img, axes=(1, 0, 2))
    compVertMinErrBoun(imgT, randimgT, overlap_size)
    
def compMinErrBoun(pre_img,top_img,cur_img,overlap_size):
    if pre_img is not None:

        compVertMinErrBoun(pre_img,cur_img,overlap_size)
    if top_img is not None:
        compHorMinErrBoun(top_img,cur_img,overlap_size)
    
def getPrevImg(i,j):
    global l_img,sample_size,overlap_size
    if j == 0:

        return None
    else:

        return l_img[(i*sample_size)-(overlap_size*i):((i+1)*sample_size)-(overlap_size*i),((j-1)*sample_size)-(j-1)*overlap_size:(j*sample_size)-(j-1)*overlap_size]

def getTopImg(i,j):
    global l_img,sample_size,overlap_size
    if i == 0:

        return None
    else:

        return l_img[((i-1)*sample_size)-(i-1)*overlap_size:(i*sample_size)-(i-1)*overlap_size,(j*sample_size)-(overlap_size*j):((j+1)*sample_size)-(overlap_size*j)]
def doqilt(pathfile):
    global im,sample_size,imglist,overlap_size,l_img
    im=cv.imread(str(pathfile),-1)


    path={}
    cost={}

    mincosts=[]
    paths={}

    x_size=500
    y_size=500

    sample_size=40
    overlap_size=10

    l_img=np.zeros((x_size,y_size,4))

    imglist=[]
    createImageList(imglist)

    cur_img=np.empty((sample_size,sample_size,4), dtype=np.float64)
    pre_img=np.empty((sample_size,sample_size,4), dtype=np.float64)
    top_img=np.empty((sample_size,sample_size,4), dtype=np.float64)

    nx=x_size/(sample_size-overlap_size)
    ny=y_size/(sample_size-overlap_size)

    newx=nx
    newy=ny



    for i in range(newx):
        for j in range(newy):
            print "value:",i,j
            pre_img = getPrevImg(i, j)
            top_img = getTopImg(i, j)

            cur_img=getminSSDImg(pre_img, top_img)

        
            x1 = (i*sample_size)-(overlap_size*i)
            x2 = ((i+1)*sample_size)-(overlap_size*i)
            y1 = (j*sample_size)-(overlap_size*j)
            y2 = ((j+1)*sample_size)-(overlap_size*j)
        
            if i == 0:
                x1 = (i*sample_size)
                x2 = ((i+1)*sample_size)
            if j == 0 :
                y1 = (j*sample_size)
                y2 = ((j+1)*sample_size)

            l_img[x1:x2,y1:y2]=cur_img
  
            mat = np.array(l_img)
            cv.imwrite('testimg.png',mat)


    mat = np.array(l_img)
    cv.imwrite('testimg.png',mat)
    return True,'testimg.png'


