import cv2
import numpy as np
import nms

img = cv2.imread("img\\a.jpg")
grayImg = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
#blur = cv2.GaussianBlur(grayImg, (5,5), 0)

kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (7, 7))
opening = cv2.morphologyEx(grayImg, cv2.MORPH_GRADIENT, kernel)
#opening = cv2.morphologyEx(grayImg, cv2.MORPH_CLOSE, kernel)
cv2.imshow("opening", opening)

img_result = cv2.adaptiveThreshold(opening, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 21, 5)
#img_result = cv2.adaptiveThreshold(opening, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 21, 5)
#ret, img_result = cv2.threshold(opening, 0, 255, cv2.THRESH_BINARY+cv2.THRESH_OTSU)
cv2.imshow("threshold", img_result)

# 테두리 팽창
closing = cv2.morphologyEx(img_result, cv2.MORPH_CLOSE, cv2.getStructuringElement(cv2.MORPH_RECT, (7, 7)))
cv2.imshow("closing", closing)

'''kernel2 = np.ones((3, 3), np.uint8)
erode = cv2.erode(closing, kernel2, iterations = 1)
cv2.imshow("erode", erode)'''

#contours, hierarchy = cv2.findContours(img_result, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
contours, hierarchy = cv2.findContours(closing, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

can = []

for i in range(len(contours)):
    x, y, w, h = cv2.boundingRect(contours[i])
    cv2.rectangle(img, (x, y), (x+w, y+h), (0, 255, 0), 2)
    if x != 0 and y != 0:
        can.append([x, y, x+w, y+h])

# nms
result = nms.non_max_suppression_fast(np.array(can), 0.3)
print(len(result))
for i in range(len(result)):
    x, y, w, h = result[i][0], result[i][1], result[i][2], result[i][3]
    cv2.rectangle(grayImg, (x,y), (w, h), (0, 255, 0), 2)

#cv2.imshow("asd2", img_result2)
#cv2.imshow("asd", img_result)
cv2.imshow("original", img)
cv2.imshow("nms", grayImg)

cv2.waitKey()
cv2.destroyAllWindows()