import cv2
import numpy as np
def fun (a,b,c1):
    #canny = cv2.Canny(blurred_image, 30, 100)
    lower_range = np.array([a, 100, 100], dtype=np.uint8)
    upper_range = np.array([b, 255, 255], dtype=np.uint8)
    mask = cv2.inRange(hsv, lower_range, upper_range)
    #cv2.imshow('mask',mask)
    ret,thresh = cv2.threshold(mask,127,255,0)
    cv2.imshow('thresh',thresh)
    im, contours, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    if len(contours) != 0:
        areas = [cv2.contourArea(c) for c in contours]
        max_index = np.argmax(areas)
        cnt=contours[max_index]
        area = cv2.contourArea(cnt)
        if area != 0:
            M = cv2.moments(cnt)
            #print M
            cx = int(M['m10']/M['m00'])
            cy = int(M['m01']/M['m00'])
            #print cx
            #print cy
            if c1 == 1 :
                cv2.putText(img, 'Red', (cx, cy), cv2.FONT_HERSHEY_SIMPLEX, 0.4, (255, 255, 255), 2, cv2.LINE_AA)
                cv2.imshow('image', img)
            if c1 == 2:
                cv2.putText(img, 'Green', (cx, cy), cv2.FONT_HERSHEY_SIMPLEX, 0.4, (255, 255, 255), 2, cv2.LINE_AA)
                cv2.imshow('image', img)
            if c1 == 3:
                cv2.putText(img, 'Blue', (cx, cy), cv2.FONT_HERSHEY_SIMPLEX, 0.4, (255, 255, 255), 2, cv2.LINE_AA)
                cv2.imshow('image', img)
        
img = cv2.imread('img0.png')
hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
cv2.imshow('bleh', img)
fun(159,189,1)
fun(44,79,2)
fun(100,130,3)
while(1):
  k = cv2.waitKey(0)
  if(k == 27):
    break
 
cv2.destroyAllWindows()

