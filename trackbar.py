# -*- coding: utf-8 -*-
"""
Created on Sun Nov  4 22:35:19 2018

@author: yea
"""
import cv2
import numpy as np
import os
 
def nothing(x):
    pass
fourcc = cv2.VideoWriter_fourcc(*'XVID')
#out = cv2.VideoWriter('output.avi',fourcc,30.0,(640,480))
cap = cv2.VideoCapture(0)
cv2.namedWindow("Trackbars")
 
cv2.createTrackbar("L - H", "Trackbars", 93, 255, nothing)
cv2.createTrackbar("L - S", "Trackbars", 94, 255, nothing)
cv2.createTrackbar("L - V", "Trackbars", 54, 255, nothing)
cv2.createTrackbar("U - H", "Trackbars", 113, 255, nothing)
cv2.createTrackbar("U - S", "Trackbars", 255, 255, nothing)
cv2.createTrackbar("U - V", "Trackbars", 219, 255, nothing)
 
 
while True:
    _, frame = cap.read()
    if not _:
        break
    # Start timer
    timer = cv2.getTickCount()

    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
 
    l_h = cv2.getTrackbarPos("L - H", "Trackbars")
    l_s = cv2.getTrackbarPos("L - S", "Trackbars")
    l_v = cv2.getTrackbarPos("L - V", "Trackbars")
    u_h = cv2.getTrackbarPos("U - H", "Trackbars")
    u_s = cv2.getTrackbarPos("U - S", "Trackbars")
    u_v = cv2.getTrackbarPos("U - V", "Trackbars")
 
    lower_blue = np.array([l_h, l_s, l_v])
    upper_blue = np.array([u_h, u_s, u_v])
    mask = cv2.inRange(hsv, lower_blue, upper_blue)
        
    kernel = np.ones((3,3),np.uint8)
    tt = cv2.erode(mask,kernel,iterations=2)
    
    result = cv2.bitwise_and(frame, frame, mask=tt)
    
    
    
    canny=cv2.Canny(result,30,60)
    cnts,contours,hierarchy  = cv2.findContours(canny, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    box1=[]
    x1=0
    y1=0
    w1=0
    h1=0
    max=0
    for i in range(len(contours)):
        cnt=contours[i]          
        x,y,w,h = cv2.boundingRect(cnt)   
        #cv2.rectangle(frame,(x,y),(x+w,y+h),(0,255,0),0)
        rect_area=w*h
        if(rect_area>max):
            max = rect_area
            x1 = x
            y1 = y
            w1 = w
            h1 = h
    cv2.rectangle(frame,(x1,y1),(x1+w1,y1+h1),(0,255,0),0)     
    # Calculate Frames per second (FPS)
    fps = cv2.getTickFrequency() / (cv2.getTickCount() - timer);
    cv2.putText(frame, "FPS : " + str(int(fps)), (100,50), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (50,170,50), 2);                        
    cv2.imshow("frame", frame)
    cv2.imshow('erode',result)
    cv2.imshow("mask", canny)
    #out.write(frame)

    key = cv2.waitKey(1)
    if key == 27:
        break
 
cap.release()
cv2.destroyAllWindows()
