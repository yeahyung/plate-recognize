import cv2
import numpy as np
import pytesseract
from  PIL import Image

class Recognition:
     def ExtractNumber(self):
          imageName = 'k1.jpg'
          Number='c:\\'+imageName
          img=cv2.imread(Number,cv2.IMREAD_GRAYSCALE)
          print(Number)
          wi, hi = img.shape[:2]
          min=0;
          if(wi<500):
              min = 300
          else:
              min = wi/3.5
          copy_img=img.copy()
          copy2_img=img.copy()
          img2=img
          cv2.imwrite('gray.jpg',img2)
          cv2.imshow('gray',img2)
          blur = cv2.GaussianBlur(img2,(5,5),0) 
          
          cv2.imwrite('blur.jpg',blur)
          cv2.imshow('GaussianBlur',blur)
          canny=cv2.Canny(blur,40,70 )
          
          cv2.imshow('canny',canny)
    #      canny=cv2.adaptiveThreshold(blur,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C,cv2.THRESH_BINARY,25,5)
         # ret,canny = cv2.threshold(blur,0,255,cv2.THRESH_BINARY+cv2.THRESH_OTSU)
          cv2.imwrite('canny.jpg',canny)
          cnts,contours,hierarchy  = cv2.findContours(canny, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

          box1=[]
          f_count=0
          select=0
          last = 0
          plate_width=0
          
          for i in range(len(contours)):
               cnt=contours[i]          
               area = cv2.contourArea(cnt) 
               x,y,w,h = cv2.boundingRect(cnt)
               rect_area=w*h  #area size
               aspect_ratio = float(h)/float(w) # ratio = height/width
               cv2.rectangle(copy2_img,(x,y),(x+w,y+h),(0,255,0),0)
               if  (aspect_ratio>=0.8)and(aspect_ratio<=5.0)and(rect_area>=240)and(rect_area<=2500):                
                    cv2.rectangle(img,(x,y),(x+w,y+h),(0,255,0),0)
                    box1.append(cv2.boundingRect(cnt))
          for i in range(len(box1)): ##Buble Sort on python
               for j in range(len(box1)-(i+1)):
                    if box1[j][0]>box1[j+1][0]:
                         temp=box1[j]
                         box1[j]=box1[j+1]
                         box1[j+1]=temp
    
         #to find number plate measureing length between rectangles
          for m in range(len(box1)):
            #   print('box1[',m,']',box1[m][0])
               count=0
               for n in range(m+1,(len(box1))):
                    delta_x=abs(box1[n][0]-box1[m][0])
                    if delta_x >min:
                         
                         break
                    delta_y =abs(box1[n][1]-box1[m][1])
                    if delta_x ==0:
                         delta_x=1
                    if delta_y ==0:
                         delta_y=1           
                    gradient =float(delta_y) /float(delta_x)
                    if gradient<0.2 or delta_y < 10:
                      #  print(count,m,n)
                        count=count+1
                    delta_x2 = delta_x
               #measure number plate size         
               if count > f_count:
                    select = m
                    f_count = count;
                    last = n
        #  print('fcount',f_count)
         # print(box1[0][0],box1[0][1],box1[0][2],box1[0][3])
          cv2.imwrite('allbox.jpg',copy2_img)
          cv2.imshow('allBounds',copy2_img)
          cv2.imwrite('snake.jpg',img)
          cv2.imshow('candidate',img)
          #cv2.imshow('snake',img)
          height=0
          if(box1[select][3]+box1[select][1]>box1[last-1][3]+box1[last-1][1]):
              height = box1[select][3]+box1[select][1]
          else:
              height = box1[last-1][3]+box1[last-1][1]
 
          number_plate=copy_img[box1[select][1]-6:height+3,box1[select][0]-3:box1[last-1][0]+box1[last-1][2]+9] 

          resize_plate=cv2.resize(number_plate,None,fx=2.0,fy=2.0,interpolation=cv2.INTER_CUBIC+cv2.INTER_LINEAR) 
          cv2.imwrite('resize_plate.jpg',resize_plate)
          cv2.imshow('plate',resize_plate)

          plate_blur=cv2.GaussianBlur(resize_plate,(5,5),0)
        #  ret,th_plate = cv2.threshold(plate_blur,50,150,cv2.THRESH_BINARY)
       #   th_plate = cv2.adaptiveThreshold(plate_blur,240,cv2.ADAPTIVE_THRESH_GAUSSIAN_C,cv2.THRESH_BINARY,41,20)
          ret,th_plate = cv2.threshold(plate_blur,0,255,cv2.THRESH_BINARY+cv2.THRESH_OTSU)
          
          cv2.imwrite('ho_plate.jpg',th_plate)
          cv2.imshow('threshold plate',th_plate)
          kernel = np.ones((3,3),np.uint8)
          er_plate = cv2.erode(th_plate,kernel,iterations=1)
          
          er_invplate = er_plate
          cv2.imwrite('er_ho_plate.jpg',er_invplate)
          cv2.imshow('er',er_invplate)
          result = pytesseract.image_to_string(er_invplate, lang='ho+car2')
          
          return(result.replace(" ",""))

recogtest=Recognition()
result=recogtest.ExtractNumber()
if(len(result) is 0):
    print('인식 실패')
elif len(result)>7:
    if (result[0] is "."):
        print('인식결과: ',result[1:len(result)])
    else:
        print('인식결과: ',result[0:7]) 
else:        
    if (result[0] is "."):
        print('인식결과: ',result[1:len(result)])
    else:
        print('인식결과: ',result) 
cv2.waitKey()


