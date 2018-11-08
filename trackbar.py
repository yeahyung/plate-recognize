# -*- coding: utf-8 -*-
"""
Created on Sun Nov  4 22:35:19 2018

@author: yea
"""
import cv2
import numpy as np
 
def nothing(x):
    pass
fourcc = cv2.VideoWriter_fourcc(*'XVID')
out = cv2.VideoWriter('output.avi',fourcc,30.0,(640,480))
cap = cv2.VideoCapture(0)
cv2.namedWindow("Trackbars")
 
cv2.createTrackbar("L - H", "Trackbars", 93, 179, nothing)
cv2.createTrackbar("L - S", "Trackbars", 94, 255, nothing)
cv2.createTrackbar("L - V", "Trackbars", 54, 255, nothing)
cv2.createTrackbar("U - H", "Trackbars", 113, 179, nothing)
cv2.createTrackbar("U - S", "Trackbars", 255, 255, nothing)
cv2.createTrackbar("U - V", "Trackbars", 219, 255, nothing)
 
 
while True:
    _, frame = cap.read()
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
 
    
    result = cv2.bitwise_and(frame, frame, mask=mask)
    canny=cv2.Canny(result,40,70 )
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
        rect_area=w*h
        if(rect_area>max):
            max = rect_area
            x1 = x
            y1 = y
            w1 = w
            h1 = h
    cv2.rectangle(frame,(x1,y1),(x1+w1,y1+h1),(0,255,0),0)                                
    cv2.imshow("frame", frame)
    cv2.imshow("mask", mask)
    out.write(frame)
    cv2.imshow("result", canny)
 
    key = cv2.waitKey(1)
    if key == 27:
        break
 
cap.release()
cv2.destroyAllWindows()
