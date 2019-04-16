# -*- coding: utf-8 -*-
"""
Created on Sat Mar 30 09:47:27 2019

@author: MFYDUCK
"""

from PIL import ImageGrab as ig

import numpy as np
import time
import cv2
import math


def mfy(img):
    """
    furkan 2 serit arasında durması gerektiğinde true vericek
    durması gerekmezse false vericek
    (!piksel degerlerinde sıkıntı var,bu sorun çözülmeli)
    """
    
    #RESMİ BELLEĞE ALMAK
    
    #2.yol
    #cv2 
    # Load an color image in grayscale
              
    #------------------------------------------------------------------------------
    #KENAR ALGILAMA
    # Burada gri tonlamaya dönüştür. 
    gray_image = cv2.cvtColor (img, cv2.COLOR_RGB2GRAY)
    # Canny Edge Detection'ı buradan arayın. 
    cannyed_image = cv2.Canny (gray_image, 60, 120)
    
    #------------------------------------------------------------------------------
    #RESMİN İLGİLİ BÖLGESİNİ ALMAK
    
    height, width, channels = img.shape
    region_of_interest_vertices = [(0, height-int(height*0.041)),
                              (0, height-int(height*0.2)),
                              (int(width/2)-int(width*0.078),height-int(height*0.416)),
                              (int(width/2) + int(width*0.078),height-int(height*0.416)),
                              (width,height-int(height*0.2)),
                              (width,height-int(height*0.041)),]
    #daha sonra bulunan noktaları matris olarak vermeliyim
    #------------------------------------------------------------------------------
    #RESMİN İLGİLİ BÖLGESİNİ KIRPMAK
    def region_of_interest(img, vertices):
        # Define a blank matrix that matches the image height/width.
        mask = np.zeros_like(img)
        # Retrieve the number of color channels of the image.
        channel_count = 4
        # Create a match color with the same color channel counts.
        match_mask_color = (255,) * channel_count
          
        # Fill inside the polygon
        cv2.fillPoly(mask, vertices, match_mask_color)
        
        # Returning the image only where mask pixels match
        masked_image = cv2.bitwise_and(img, mask)
        
        return masked_image
    
    
    cropped_image = region_of_interest(cannyed_image,np.array([region_of_interest_vertices], np.int32),)

    #------------------------------------------------------------------------------
    #KENAR piksellerinden serit oluşturmak
    lines = cv2.HoughLinesP(cropped_image,rho=6,theta=np.pi / 60,threshold=160,lines=np.array([]),
        minLineLength=40,maxLineGap=25)
    #------------------------------------------------------------------------------
    #LİNES DEGERLERİ İLE ORJİNAL RESİMDE SERİT ÇİZİMİ
    def draw_lines(img, lines, color=[0, 0, 255], thickness=3):
        # If there are no lines to draw, exit.
        if lines is None:
            return
        # Make a copy of the original image.
        img = np.copy(img)
        # Create a blank image that matches the original in size.
        line_img = np.zeros((img.shape[0],img.shape[1],channels),dtype=np.uint8,)
        # Loop over all lines and draw them on the blank image.
        for line in lines:
            for x1, y1, x2, y2 in line:
                cv2.line(line_img, (x1, y1), (x2, y2), color, thickness)
                # Merge the image with the lines onto the original.
        
                img = cv2.addWeighted(img,0.8,line_img,1.0, 0.0)
                # Return the modified image.
        return img


    #---------------------------------------------------------------------------------------
    min_line_y = 0
    max_line_y = height
    piksel1=0
    piksel2=1000
    for line in lines:
        for x1, y1, x2, y2 in line:
            slope = (y2 - y1) / (x2 - x1) # <-- Calculating the slope.
            if math.fabs(slope) > 0.1: # <-- Only consider extreme slope,eğim yatay değilse cık
                continue
            if int((y1+y2)/2) > min_line_y :  # <-- Otherwise, right group.
                min_line_y=int((y1+y2)/2)
                
            if int((y1+y2)/2) < max_line_y :
                max_line_y=int((y1+y2)/2)
                    
    piksel1=height-min_line_y
    #cv2.putText(img,"yakin serit"+str(piksel1),(100,100), cv2.FONT_HERSHEY_SIMPLEX,2.0, (0, 255, 255), 3)
    #img = draw_lines(img,[[[int(width/2),int(height),int(width/2),min_line_y],]],[0,255,255],5)
    if  max_line_y+int(height*0.03)< min_line_y:
        piksel2=height-max_line_y 
        #cv2.putText(img,"uzak serit"+str(piksel2),(100,200), cv2.FONT_HERSHEY_SIMPLEX,2.0, (0, 0, 255), 3)
        #img = draw_lines(img,[[[int(width/2)+20,int(height),int(width/2)+20,max_line_y ],]],[0,0,255],5)
    if piksel1<int(height*0.30):#150-132
        if piksel2<int(height*0.50):#270-240
            #cv2.putText(img,"True",(100,300), cv2.FONT_HERSHEY_SIMPLEX,2.0, (0, 0, 255), 3)
            return True
        else:
            #cv2.putText(img,"False",(100,400), cv2.FONT_HERSHEY_SIMPLEX,2.0, (0, 0, 255), 3)
            return False
    else:
        #cv2.putText(img,"False",(100,500), cv2.FONT_HERSHEY_SIMPLEX,2.0, (0, 0, 255), 3)
        return False
            
