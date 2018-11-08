import cv2
import numpy as np

cap = cv2.VideoCapture(0)
if(cap.isOpened() == False):
    print("Unable to read  camera")

while True:
    ret, frame = cap.read()
    removeNoise = cv2.GaussianBlur(frame,(5,5),0) 
    hsv = cv2.cvtColor(removeNoise,cv2.COLOR_BGR2HSV)
    
    lower = np.array([70,50,70])
    upper = np.array([120,255,255])
    
    mask = cv2.inRange(hsv,lower,upper)
    
    res = cv2.bitwise_and(frame,frame,mask=mask)
    
    cv2.imshow('test',hsv)
    
    k = cv2.waitKey(1)
    if k==27:
        break;
cap.release()
cv2.destroyAllWindows()