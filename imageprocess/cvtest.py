# -*- coding: utf-8 -*- 
'''
Created on 2013-12-8

@author: GroundMelon
'''
import cv2
import numpy as np
from matplotlib import pyplot as plt




wincount = 0

def win(*img_list):
    global wincount
    for img in img_list:
        cv2.imshow('win%d'%wincount,img)
        wincount += 1

if __name__ =='__main__':
    #------ Main  ------
    print('OpenCV is %soptimized'%('' if cv2.useOptimized() else 'not '))
    
    img_name = r'color\colorruler.jpg'
    img = cv2.imread(r'F:\Workplace\GroundStation\imageprocess\%s'%img_name,cv2.IMREAD_COLOR)
    
    s = img.tostring()
    
    newimg = np.ndarray(shape=img.shape, dtype=img.dtype,buffer = s)
    cv2.imshow('',newimg)
    cv2.waitKey(0)
    
    # print(img) = [BGR(1,:);BGR(2,:);...;BGR(n,:)] 
    
    #------ matplotlib usage ------
    # plt.imshow(img[:,:,::-1], cmap = 'gray', interpolation = 'bicubic')#BGR to RGB
    # plt.show()
    
    #------ draw rectangle ------
    # cv2.rectangle(img,(100,100),(200,200),(0,0,255),1)
    # cv2.imshow(win(),img)
    
    #------ bgr split ------
    # b,g,r = img[:,:,0],img[:,:,1],img[:,:,2]
    # win(b,g,r)
    # bmask=np.zeros(img.shape, dtype=np.uint8);bmask[:,:,0] = 1;ipshell();b = img*bmask
    # gmask=np.zeros(img.shape, dtype=np.uint8);gmask[:,:,1] = 1;g = img*gmask
    # rmask=np.zeros(img.shape, dtype=np.uint8);rmask[:,:,2] = 1;r = img*rmask
    # win(b,g,r)
    
    #------ bitwise operation ------
    #img = np.array([[0x10,0x40],[0x80,0xFF]])
    #mask = np.array([[255,0],[0,255]],dtype=np.uint8)
    #print cv2.bitwise_and(img,img,mask = mask)
    #print cv2.bitwise_and(img,img,mask = cv2.bitwise_not(mask))
    
    #img2 = cv2.GaussianBlur(img,(5,5),10)
    #cv2.imshow('Gauss',img2)
    #img3 = cv2.resize(img,(img.shape[0]/2,img.shape[1]/2))
    #cv2.imshow(win(),img3)   
    #cv2.imshow('CannyGauss',cv2.Canny(img2,10,100,3))
    #cv2.imshow('CannySrc',cv2.Canny(img,10,100,3))
    
    # ----- 颜色识别-----
    # bgr = newimg.copy()
    # hsv = cv2.cvtColor(bgr, cv2.COLOR_BGR2HSV)
    # h = hsv[:,:,0]
    # selected_hue = np.average(h)
    # print selected_hue
    hsv = cv2.cvtColor(newimg, cv2.COLOR_BGR2HSV)
    mask = cv2.inRange(hsv, np.array([119,50,50]), np.array([121,255,255]))
    mask = cv2.medianBlur(mask, 5)
    
    cv2.imshow('',mask)
    cv2.waitKey(0)
    rtn = cv2.moments(mask)
    m10 = rtn['m10']
    m01 = rtn['m01']
    m00 = rtn['m00']
    print('%f,%f'%(m10/m00, m01/m00))
    
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    #raw_input('Press any key to continue...')
