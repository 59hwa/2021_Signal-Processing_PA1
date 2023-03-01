#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed May  5 12:53:22 2021

@author: sejinpark
"""
import numpy as np
import PIL.Image as pilimg
import math
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import time

start = time.time()

def Fmat(n):
    a = np.zeros((n,n),complex)
    for i in range(n):
        for j in range(n):
            a[i][j]=complex(math.cos(2*i*j*math.pi/n)-complex(0,1)*math.sin(2*i*j*math.pi/n))
    return a

def InMat(matrix):
    return matrix.conjugate()/len(matrix)

def Fourier(Mata,Matb,sample):
    i = np.matmul(Mata,sample)
    j = np.matmul(i,Matb)
    return j
def InFourier(Mata,Matb,sample):
    i = np.matmul(InMat(Mata),sample)
    j = np.matmul(i,InMat(Matb))
    return j
def Corr(samplef, data, Mata, Matb):
    ma = samplef * Fourier(Mata,Matb,data).conjugate()
    R = ma/np.abs(ma)
    r = InFourier(Mata,Matb,R)
    return np.amax(r.real)
    # return  np.amax(np.abs(r)) 실수부와 결과는 같으나 속도가 좀 느림

im = pilimg.open("/Users/sejinpark/Desktop/dataset/start.jpg").convert('L')
pix = np.array(im)
pixes = []
pixesr = []
for i in range(10):
    imager = pilimg.open("/Users/sejinpark/Desktop/dataset/0" + str((i+1)*10).zfill(3) +".jpg")
    image = imager.convert('L')
    pixssr = np.array(imager)
    pixesr.append(pixssr)
    pixss = np.array(image)
    pixes.append(pixss)

deltay=27
deltax=30
Matb=Fmat(deltax)
Mata=Fmat(deltay)
xpath = 274
ypath = 136
sample = pix[ypath:ypath+deltay,xpath:xpath+deltax]
samplef = Fourier(Mata,Matb,sample)

for l in range(10):
    # k= float('-inf') 최솟값 비교용
    k = np.zeros((len(pix)-deltay, len(pix[0])-deltax),float )
    for i in range(0,len(pix)-deltay):
        for j in range(0,len(pix[0])-deltax):
            data = pixes[l][i:i+deltay,j:j+deltax]
            k[i][j] = Corr(samplef, data, Mata, Matb)
            # activation map을 만들지 않고 최댓값 구하기 실행시간은 거의 같다.
            # if k<Corr(samplef, data, Mata, Matb):
            #     k=Corr(samplef, data, Mata, Matb)
            #     ki=i
            #     kj=j

    kn = np.where(k == max(map(max,k)))        
    ki = int(kn[0]) 
    kj = int(kn[1])
    plt.imshow(k)
    fig,ax1 = plt.subplots(1)
    ax1.imshow(pixesr[l])
    rect = patches.Rectangle((kj,ki),deltax,deltay,linewidth=1,edgecolor='r',facecolor='none')
    ax1.add_patch(rect)
    plt.show()
    samplef = Fourier(Mata, Matb, pixes[l][ki:ki+deltay,kj:kj+deltax]) #sample을 갱신하여 correlation을 실행시키려 했으나 조금이라도 빗나가기 시작하면 계속 빗나가 버림
    print("time :", time.time() - start)
print("time :", time.time() - start)
