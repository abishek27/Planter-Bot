import cv2
import numpy as np
import os
img1 = cv2.imread('img0.png')
imgray = cv2.cvtColor(img1,cv2.COLOR_BGR2GRAY)
ret,thresh = cv2.threshold(imgray,90,255,cv2.THRESH_BINARY_INV)
image, contours, hierarchy = cv2.findContours(thresh,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE) 
for i in range(len(contours)):
    cnt = contours[i]
    M = cv2.moments(cnt)
    cx = int(M['m10']/M['m00'])
    cy = int(M['m01']/M['m00'])
    epsilon = 0.01*cv2.arcLength(contours[i],True)
    approx = cv2.approxPolyDP(contours[i],epsilon,True)
    print approx
    print len(approx)
    if len(approx) == 3:
        cv2.putText(img1,str("triangle"),(cx,cy),cv2.FONT_HERSHEY_SIMPLEX,1,(0,0,0),1)
    if len(approx) == 4:
        cv2.putText(img1,str("quad"),(cx,cy),cv2.FONT_HERSHEY_SIMPLEX,1,(0,0,0),1)
    if len(approx) == 5:
        cv2.putText(img1,str("pent"),(cx,cy),cv2.FONT_HERSHEY_SIMPLEX,1,(0,0,0),1)
    if len(approx) == 6:
        cv2.putText(img1,str("hex"),(cx,cy),cv2.FONT_HERSHEY_SIMPLEX,1,(0,0,0),1)
    if len(approx) > 6:
        cv2.putText(img1,str("circle"),(cx,cy),cv2.FONT_HERSHEY_SIMPLEX,1,(0,0,0),1)
cv2.imshow('image',img1)
cv2.waitKey(0)

