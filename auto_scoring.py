# -*- coding: utf-8 -*-
from tkinter import *
from PIL import Image
from PIL import ImageTk
from tkinter import filedialog
import cv2
from skimage.measure import compare_ssim
import imutils
import numpy as np
import os
import subprocess
import pytesseract
from operator import eq
import codecs

def select1():        # 시험지 선택
    global testSheet
    path = filedialog.askopenfilename()
    testSheet = cv2.imread(path,0) # 0은 gray로 읽겠다는 의미


def select2():         # 정답 and 좌표찾기
   global answerSheet, position,answerList
   path = filedialog.askopenfilename()
   answerSheet = cv2.imread(path,0)

   # 이미지 서로 다른 부분 찾는 코드    정확히 모름
   (score, diff) = compare_ssim(testSheet,answerSheet, full=True)
   diff = (diff*255).astype("uint8")
   thresh = cv2.threshold(diff,0,255,cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)[1]
   cnts = cv2.findContours(thresh.copy(),cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
   cnts = cnts[0] if imutils.is_cv2() else cnts[1]

   # 정답지 세로로 분리
   x1,y1,h1 = 0,0,0
   num=0
   count=0
   startX,startY=0,0
   img=[]
   row=[]
   row.append([])
   box=[]
   for c in cnts:
      (x,y,w,h) = cv2.boundingRect(c)
      box.append(c)
      if count==0:
         row[num].append(count)
         pass
      else:
         if abs(y1-y)<20:
            row[num].append(count)
         else:
            num = num+1
            row.append([])
            row[num].append(count)
      y1=y
      count+=1

   #정답지 세로로 분리된 것 중에 가로로 분리할 수 있는지 확인
   a,b,c,d=0,0,0,0
   for i in range(0,len(row)):
      minX=10000
      minY=10000
      maxX=0
      maxY=0

      for j in range(0,len(row[i])):
         a,b,c,d = cv2.boundingRect(box[row[i][j]])
         if minX>a:
            minX=a
         if maxY < b + d:
            maxY = b + d
         if maxX < a + c:
            maxX = a + c
         if minY > b:
            minY = b
      if abs(maxY - minY) < 5:
         pass
      else:
         img.append(answerSheet[minY:maxY, minX:maxX])    # img == 최종 답안 단어들의 이미지를 저장한 리스트
   print(len(position))
   answerList = []

   # 이 코드가 실행하고 있는 위치에 answer이라는 폴더만들면 정답지가 answer폴더안에 저장       dir있는지 확인하고 없으면 만드는 코드로 수정
   for i in range(0, len(img)):
      #cv2.imshow(str(i), img[i])
      # resize = cv2.resize(img[i], None, fx=2.0, fy=2.0, interpolation=cv2.INTER_CUBIC + cv2.INTER_LINEAR)

      '''gau = cv2.GaussianBlur(resize, (5, 5), 0)
      temp = cv2.addWeighted(resize, 1.5, gau, -0.5, 0)

      kernel = np.ones((2,2), np.uint8)
      er = cv2.erode(temp, kernel, iterations=1)'''

      #cv2.imshow("zzz", er)
      #tessdata_dir_config = r'--tessdata-dir "<C:\Program Files (x86)\Tesseract-OCR\tessdata>"'

      #cv2.imwrite("answer\\"+"ss"+str(i) + ".jpg", er)
      result = pytesseract.image_to_string(img[i],lang='eng')
      result = result.replace(" ","")
      result = str(result)
      answerList.append(result)
      print(result)

   if not (os.path.isdir("answerSheet")):
      os.makedirs(os.path.join("answerSheet"))

   '''f = open("answerSheet/answerList.txt","w",-1,"utf-8")
   for i in range(0,len(answerList)):
      f.write(answerList[i]+"\n")
   f.close()'''

   #cv2.waitKey(0)  # esc키 누르면 나온 답지 꺼짐
   #cv2.destroyAllWindows()

def select3():         # 학생들 정답 찾기 & 정답과 비교, 채점해서 출력
   global studentSheet
   studentAnswer = []
   path = filedialog.askopenfilename()
   studentSheet = cv2.imread(path,0)
   if not (os.path.isdir("answer")):
      os.makedirs(os.path.join("answer"))
   '''for i in range(0,len(position)):
      studentAnswer.append(studentSheet[position[i][0]:position[i][1],position[i][2]:position[i][3]])
      cv2.imwrite("answer\\"+str(i)+".jpg",studentAnswer[i])'''

   #cv2.imshow("test",testSheet)
   #cv2.imshow("answer",answerSheet)
   #cv2.imshow("student",studentSheet)

   # 이미지 서로 다른 부분 찾는 코드    정확히 모름
   (score, diff) = compare_ssim(testSheet, studentSheet, full=True)
   diff = (diff * 255).astype("uint8")
   thresh = cv2.threshold(diff, 0, 255, cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)[1]
   cnts = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
   cnts = cnts[0] if imutils.is_cv2() else cnts[1]

   # 정답지 세로로 분리
   x1, y1, h1 = 0, 0, 0
   num = 0
   count = 0
   startX, startY = 0, 0
   img2 = []
   row2 = []
   row2.append([])
   box2 = []
   for c in cnts:
      (x, y, w, h) = cv2.boundingRect(c)
      box2.append(c)
      if count == 0:
         row2[num].append(count)
         pass
      else:
         if abs(y1 - y) < 20:
            row2[num].append(count)
         else:
            num = num + 1
            row2.append([])
            row2[num].append(count)
      y1 = y
      count += 1

   zz=cv2.imread(path,1)
   # 정답지 세로로 분리된 것 중에 가로로 분리할 수 있는지 확인
   a, b, c, d = 0, 0, 0, 0
   for i in range(0, len(row2)):
      minX = 10000
      minY = 10000
      maxX = 0
      maxY = 0

      for j in range(0, len(row2[i])):
         a, b, c, d = cv2.boundingRect(box2[row2[i][j]])
         if minX > a:
            minX = a
         if maxY < b + d:
            maxY = b + d
         if maxX < a + c:
            maxX = a + c
         if minY > b:
            minY = b
      if abs(maxY - minY) < 5:
         pass
      else:
         img2.append(studentSheet[minY:maxY, minX:maxX])  # img == 최종 답안 단어들의 이미지를 저장한 리스트
         cv2.rectangle(zz,(minX,minY),(maxX,maxY),(0,0,255),3)
         pos = []
         pos.append(minY)
         pos.append(maxY)
         pos.append(minX)
         pos.append(maxX)
         position.append(pos)
   cv2.imwrite("myanswe.jpg",zz)
   for i in range(0, len(img2)):
      cv2.imwrite("C:\\Users\\yea\\.spyder-py3\\answer\\"+""+str(i) + ".jpg", img2[i])
   os.chdir("C:\\Users\yea\Desktop\SimpleHTR-master\src")
   os.system('activate yolo & python main.py')           # main.py 실행하면 answerImage에 있는 폴더 모두 실행, txt파일에 정답 저장

   # blank 처리 - len(answerList) - studentAnswerList
   #r = open('C:\\Users\yea\.spyder-py3\\answerSheet\\answerwordLists.txt','rt')
   with codecs.open('C:\\Users\yea\.spyder-py3\\answerSheet\\answerwordLists.txt','r') as r:
      while(1):
         line = r.readline()
         try:escape=line.index('\n')
         except:escape=len(line)

         if line:
            studentAnswer.append(line[0:escape].replace(" ",""))
         else:
            break
   r.close()
   answerList1 = []
   with codecs.open('C:\\Users\yea\.spyder-py3\\answerSheet\\answerList.txt','r',encoding='utf-8') as g:
      while(1):
         line = g.readline()
         try:escape=line.index('\r\n')
         except:
            escape = len(line)

         if line:
            answerList1.append(line[0:escape].replace(" ", ""))
         else:
            break
   g.close()

   print(answerList1)
   print(studentAnswer)

   score = len(studentAnswer)
   correctNum = np.zeros(len(answerList1))
   '''for i in range(0,len(studentAnswer)):
      correct = 0
      for j in range(0,len(answerList)):              # answerList는 순서대로 저장되 있으므로 j에 따라 채점
         if(studentAnswer[i] == answerList[j]):
            correct = 1
            correctNum[j]=1
            break
      if correct==0:ZZ
         print(studentAnswer[i])
         score-=1'''
   for item in studentAnswer:
      correct = 0
      for j in range(0,len(answerList1)):
         if eq(item,answerList1[j]):
            correct = 1
            correctNum[j] = 1
      if correct==0:
         print(item)
         score-=1
   print(score)
   print(correctNum)
   color = cv2.imread(path)
   for i in range(0,len(correctNum)):
      if(correctNum[i] == 1):
         print("correct!")
         #print(img2[i][0],img2[i][1])
         cv2.circle(color,(int((position[i][3]+position[i][2])/2),int((position[i][0]+position[i][1])/2)),30,(0,0,255),5)
         #cv2.circle(studentSheet,(int(x+w/2),int(y-h/2)),30,(0,0,255),-1)
      else:
         cv2.putText(color," / ", (int((position[i][3]+position[i][2])/2)-70,int((position[i][0]+position[i][1])/2)+35), cv2.FONT_HERSHEY_PLAIN, 5, (0, 0, 255), 5, cv2.LINE_AA)

   cv2.putText(color,str(score) + " / " + str(len(correctNum)), (1070,1950),cv2.FONT_HERSHEY_SIMPLEX,3,(0,0,255),5,cv2.LINE_AA)
   color = cv2.resize(color,(850,850))
   cv2.imshow("Result",color)
   cv2.imwrite("Result.jpg",color)
   # cv2.circle(img,(447,63), 63, (0,0,255), -1)

   cv2.waitKey(0)
   cv2.destroyAllWindows()


# initialize the window toolkit along with the two image panels
root = Tk()

testSheet = None
answerSheet = None
studentSheet = None
position = []
answerList = []


# create a button, then when pressed, will trigger a file chooser
# dialog and allow the user to select an input image; then add the
# button the GUI
btn = Button(root, text="Select student's answer", command=select3)     # button누르면 select3 실행됨
btn.pack(side="bottom", fill="both", expand="yes", padx="10", pady="10")

btn1 = Button(root, text="Select answer sheet", command=select2)
btn1.pack(side="bottom", fill="both", expand="yes", padx="10", pady="10")

btn2 = Button(root, text="Select test sheet", command=select1)
btn2.pack(side="bottom", fill="both", expand="yes", padx="10", pady="10")

# kick off the GUI
root.mainloop()