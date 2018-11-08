import cv2
import numpy as np
img = cv2.imread('C:\\Users\\yea\\phone.jpg')
x = 160
width = 120
y = 180
height = 225
roi = img[y:y+height,x:x+width]
# r == y c== x
track_window = (x,y,width,height)
hsv_roi = cv2.cvtColor(roi,cv2.COLOR_BGR2HSV)
mask = cv2.inRange(hsv_roi, np.array((0.,60.,32.)),np.array((180.,255.,255.)))
roi_hist = cv2.calcHist([hsv_roi],[0],mask,[180],[0,180])
cv2.normalize(roi_hist,roi_hist,0,255,cv2.NORM_MINMAX)
cap = cv2.VideoCapture(0)

term_criteria = (cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT,10,1)

while True:
    _,frame = cap.read()
    hsv = cv2.cvtColor(frame,cv2.COLOR_BGR2HSV)
    dst = cv2.calcBackProject([hsv],[0],roi_hist,[0,180],1)
    
    ret, track_window = cv2.CamShift(dst,track_window,term_criteria)
    
    pts = cv2.boxPoints(ret)
    pts = np.int0(pts)
    img2 = cv2.polylines(frame,[pts],True,(255,0,0),2)
    cv2.imshow('img2',img2)
    cv2.imshow("frame",frame)
    
    key = cv2.waitKey(1)
    if key==27:
        break;
    
cap.release()
cv2.destroyAllWindows()