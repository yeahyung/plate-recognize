import cv2
import matplotlib.pyplot as plt
from darkflow.net.build import TFNet

options ={
    'model':'cfg/yolo.cfg',
    'load':'bin/yolov2.weights',
    'threshold':0.3
}
tfnet = TFNet(options)

img = cv2.imread('sample_img/sample_horses.jpg',1)
img = cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
result = tfnet.return_predict(img)

for i in range(len(result)):
    tl = (result[i]['topleft']['x'],result[i]['topleft']['y'])
    br = (result[i]['bottomright']['x'],result[i]['bottomright']['y'])
    label = result[i]['label']
    img = cv2.rectangle(img, tl, br, (0, 255, 0), 7)
cv2.imshow('asd',img)
cv2.waitKey()
