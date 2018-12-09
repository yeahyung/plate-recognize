# -*- coding: utf-8 -*-
"""
Created on Sun Nov  4 22:35:19 2018

@author: yea
"""
import cv2
import numpy as np
import os

import RPi.GPIO as GPIO
from time import sleep

#Hyper parameter
iHeight = 270

#Pin setup parameter
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
STOP = 0
FORWARD = 1

CH1 = 0 # left Motor
CH2 = 1 # right Motor

OUTPUT = 1
INPUT = 0

HIGH = 1
LOW = 0

# PWM PIN
ENA = 26  # 37 pin
ENB = 21  # 27 pin

# GPIO PIN
IN1 = 19  # 37 pin
IN2 = 13  # 35 pin
IN3 = 16  # 31 pin
IN4 = 20  # 29 pin


def setPinConfig(EN, INA, INB):
    GPIO.setup(EN, GPIO.OUT)
    GPIO.setup(INA, GPIO.OUT)
    GPIO.setup(INB, GPIO.OUT)

    pwm = GPIO.PWM(EN, 100)

    pwm.start(0)
    return pwm


def setMotorControl(pwm, INA, INB, speed): 
    pwm.ChangeDutyCycle(speed)
    GPIO.output(INA, 1)
    GPIO.output(INB, 0)

def setMotor(ch, speed): # set Motor speed
    if ch == CH1:
        setMotorControl(pwmA, IN1, IN2, speed)
    else:
        setMotorControl(pwmB, IN3, IN4, speed)

# get motoer direction  
def getDirection(differX, direction):
    # need adjustment
    if direction == "r":
        if (differX > 0):
            return int(differX*-0.12)
        else:
            return 0
    else:
        if (differX < 0):
            return int(differX*0.12)
        else:
            return 0
    return 0
   
def nothing(x):
    pass

#Buzz pin setup
GPIO.setup(3,GPIO.OUT)
bz_pwm=GPIO.PWM(3, 1000)

# set Motor configuration
pwmA = setPinConfig(ENA, IN1, IN2)
pwmB = setPinConfig(ENB, IN3, IN4)

#open camera
cap = cv2.VideoCapture(0)
#cv2.namedWindow("Trackbars")

while True:
    _, frame = cap.read()
    if not _:
        break
    # Start timer
    # timer = cv2.getTickCount()
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    l_h = 50
    l_s = 123
    l_v = 90
    u_h = 215
    u_s = 255
    u_v = 208

    lower_blue = np.array([l_h, l_s, l_v])
    upper_blue = np.array([u_h, u_s, u_v])
    mask = cv2.inRange(hsv, lower_blue, upper_blue)

    result = cv2.bitwise_and(frame, frame, mask=mask)
    canny=cv2.Canny(result,20,80 )
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
    #Control movement
    differX = int((((2*x1)+w1)/2)-320)
    height = h1
    
    #go
    #need adjutment
    differ = iHeight - height 
    go=0
    #stop, close
    if differ < 0:  
        go=0
    #running   differ < iHeight*0.9
    elif differ > 0:
        go=99
    #cant find
    else:
        go=0

    #rspeed
    if (differX > 0):
        para = -0.25
        if(differX>170):
            para = -0.1
        rspeed = go + int(differX*para)
        if rspeed<0:
	rspeed=0
    else:
        rspeed = go

    #lspeed
    if(differX<0):
        para = 0.25
        if(differX<-170):
            para = 0.1
        lspeed =go + int(differX*para)
        if lspeed<0:
            lspeed=0
        #lspeed-=30
    else:
        lspeed = go
        #lspeed -=30
  
    if(max==0):
        #buzzr ring
        lspeed=0
        rspeed=0
        bz_pwm.start(100)
        bz_pwm.ChangeDutyCycle(90)
        bz_pwm.ChangeFrequency(500)
        sleep(0.2)
        bz_pwm.stop()
    print(differX)
    setMotor(CH1, rspeed)
    setMotor(CH2, lspeed)

    cv2.rectangle(frame, (x1, y1), (x1 + w1, y1 + h1), (0, 255, 0), 0)

    # x1 : ÁÂÃø xÁÂÇ¥ y1: ÁÂÃø yÁÂÇ¥ w1 ³Êºñ h1 ³ôÀÌ

    # Calculate Frames per second (FPS)
    '''fps = cv2.getTickFrequency() / (cv2.getTickCount() - timer);
    cv2.putText(frame, "FPS : " + str(int(fps)), (100,50), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (50,170,50), 2);   
    cv2.imshow("mask", mask)                     
    cv2.imshow('erode',result)
    cv2.imshow("masssk", canny)'''
    cv2.imshow("frame", frame)
    # out.write(frame)

    key = cv2.waitKey(1)
    if key == 27:
        break

cap.release()
cv2.destroyAllWindows()