import cv2
import numpy as np
import time
import copy

imageName = "6.jpg"
start_time = time.time()
large = cv2.imread("img\\"+imageName)
#large = cv2.pyrUp(large)
#rgb = cv2.pyrDown(large)
small = cv2.cvtColor(large, cv2.COLOR_BGR2GRAY)

kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3, 3))
grad = cv2.morphologyEx(small, cv2.MORPH_GRADIENT, kernel)

_, bw = cv2.threshold(grad, 0.0, 255.0, cv2.THRESH_OTSU+cv2.THRESH_BINARY)
cv2.imshow("bw", large)
kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (8, 2))
connected = cv2.morphologyEx(bw, cv2.MORPH_CLOSE, kernel)
# using RETR_EXTERNAL instead of RETR_CCOMP
#contours, hierarchy = cv2.findContours(connected.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
contours, hierarchy = cv2.findContours(connected.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
#For opencv 3+ comment the previous line and uncomment the following line
#_, contours, hierarchy = cv2.findContours(connected.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)


mask = np.zeros(bw.shape, dtype=np.uint8)
temp = []
for idx in range(len(contours)):
    x, y, w, h = cv2.boundingRect(contours[idx])
    mask[y:y+h, x:x+w] = 0
    cv2.drawContours(mask, contours, idx, (255, 255, 255), -1)
    r = float(cv2.countNonZero(mask[y:y+h, x:x+w])) / (w * h)

    if r > 0.35 and w > 5 and h > 5 and w < 200 and h < 200:
        #cv2.rectangle(large, (x, y), (x+w-1, y+h-1), (0, 255, 0), 2)
        temp.append(contours[idx])

# small image검은색으로 바꾸기
for i in range(len(small)):
    small[i] = 0

# box의 중심점 빨간점 찍고 grid detect
for idx in range(len(temp)):
    x, y, w, h = cv2.boundingRect(temp[idx])
    centerX = x+int(w/2)
    centerY = y+int(h/2)
    cv2.circle(small, (centerX, centerY), 10, (255, 255, 0), 5)
    cv2.rectangle(large, (x, y), (x+w-1, y+h-1), (0, 255, 0), 2)

# centerX로 정렬한 걸 axisX에 저장
axisX = copy.deepcopy(temp)
for i in range(len(axisX)-1):
    for j in range(len(axisX)-1-i):
        x, y, w, h = cv2.boundingRect(axisX[j])
        centerX = int(x+w/2)
        centerY = y+h/2
        x1, y1, w1, h1 = cv2.boundingRect(axisX[j+1])
        centerX1 = int(x1+w1/2)
        centerY1 = y1+h1/2
        if centerX > centerX1:
            tempo = axisX[j]
            axisX[j] = axisX[j+1]
            axisX[j+1] = tempo

for i in range(len(axisX)):
    x,y,w,h, = cv2.boundingRect(axisX[i])
    centerX = x + int(w / 2)
    centerY = y + int(h / 2)
    cv2.putText(small, str(i), (centerX+10, centerY), cv2.FONT_HERSHEY_PLAIN, 2, (255, 255, 0), 2, cv2.LINE_AA)

# 가로, 세로로 연결된 점들의 집합 count하기
countList = np.zeros((len(axisX)+1, len(axisX)+1))
for i in range(len(axisX)):
    x, y, w, h = cv2.boundingRect(axisX[i])
    maxX = x + w/2
    minX = x + w/2
    maxY = y + h/2
    minY = y + h/2
    for j in range(i+1, len(axisX)):
        x1, y1, w1, h1 = cv2.boundingRect(axisX[j])
        positionX1 = x1 + w1/2
        positionY1 = y1 + h1/2

        if (abs(minX-positionX1) < 10 and abs(minY - positionY1) < 3*h1) or (abs(maxX-positionX1) < 10 and abs(maxY -
                                                                                                  positionY1) < 3*h1):
            if countList[i + 1][j + 1] == 0:
                countList[i+1][j+1] = 1        # 서로 연결돼어있다.
                countList[j+1][i+1] = 1
            else:
                countList[i + 1][j + 1] = 3  # 서로 연결돼어있다.
                countList[j + 1][i + 1] = 3
            countList[i+1][0] += 1           # 연결된 점의 개수 +1 추가
            countList[j+1][0] += 1
            if positionY1 < minY:
                minY = positionY1
                minX = positionX1
            elif positionY1 > maxY:
                maxY = positionY1
                maxX = positionX1

for i in range(len(axisX)):
    x, y, w, h = cv2.boundingRect(axisX[i])
    positionX = x + w/2
    positionY = y + h/2
    for j in range(i+1, len(axisX)):
        x1, y1, w1, h1 = cv2.boundingRect(axisX[j])
        positionX1 = x1 + w1/2
        positionY1 = y1 + h1/2

        if abs(positionY - positionY1) < 15 and abs(positionX - positionX1) < 4 * w1:
        # countList[i + 1][j + 1] += 2  # 서로 연결돼어있다.
        # countList[j + 1][i + 1] += 2
            if countList[i + 1][j + 1] == 0:
                countList[i + 1][j + 1] = 2
                countList[j + 1][i + 1] = 2
            else:
                countList[i + 1][j + 1] = 3
                countList[j + 1][i + 1] = 3
            countList[i + 1][0] += 1
            countList[j + 1][0] += 1
            positionX = positionX1
            positionY = positionY1

for i in range(1, len(countList)):
    count = countList[i][0]
    colX = 0
    colY = 0
    lastX = 0
    lastY = 0
    for j in range(i+1, len(countList)):
        if count >= 2 and abs(count - countList[j][0]) <= 3 and (countList[i][j] == 1 or countList[i][j] == 3 or
                                                                 countList[j][i] == 1 or countList[j][i] == 3):
            colY += 1
            lastY = j
        elif count >= 2 and abs(count - countList[j][0]) <= 3 and (countList[i][j] == 2 or countList[i][j] == 3 or
                                                                   countList[j][i] == 1 or countList[j][i] == 3):
            colX += 1
            lastX = j

    if colX >= 2 and colY >= 2:
        x, y, w, h = cv2.boundingRect(axisX[i])
        x1, y1, w1, h1 = cv2.boundingRect(axisX[lastX])
        x2, y2, w2, h2 = cv2.boundingRect(axisX[lastY])
        newImg = large[y:y2-h2, x:x1+w1]
        cv2.imwrite("result3\\"+str(i)+str(j)+".jpg", newImg)

print("%s seconds" % (time.time()-start_time))
cv2.imshow("small",small)
cv2.imshow('rects', large)
cv2.imwrite("result2\\"+imageName,small)
cv2.waitKey(0)
cv2.destroyAllWindows()