import cv2
import os
from picamera import PiCamera
from picamera.array import PiRGBArray
import numpy as np
import time
from time import sleep

start_time = time.time()
prev_time = time.time()
###########################################################################

import RPi.GPIO as GPIO
count = 0
i = 0
a=0
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)
 
Motor1A = 33
Motor1B = 35
Motor1E = 37
Motor2A = 36
Motor2B = 38
Motor2E = 40

GPIO.setup(Motor1A,GPIO.OUT)
GPIO.setup(Motor1B,GPIO.OUT)
GPIO.setup(Motor1E,GPIO.OUT)
GPIO.setup(Motor2A,GPIO.OUT)
GPIO.setup(Motor2B,GPIO.OUT)
GPIO.setup(Motor2E,GPIO.OUT)

right = GPIO.PWM(Motor1E, 100)
left = GPIO.PWM(Motor2E, 100)
left.start(15)
right.start(15)

###########################################################################

fourcc = cv2.VideoWriter_fourcc(*'XVID')
cam = PiCamera()
cam.resolution = (160,120)

cam.framerate = 30
raw_cap = PiRGBArray(cam,(160,120))
frame_cnt = 0

kp = 1
kd = 0
set_point = 80
pwm1 = 10
pwm2 = 10
previous_error = 0

sleep(1)

for frame in cam.capture_continuous(raw_cap,format="bgr",use_video_port=True,splitter_port=2,resize=(160,120)):
    
    color_image = frame.array
    

    gray = cv2.cvtColor(color_image, cv2.COLOR_BGR2GRAY)
    ret,thresh = cv2.threshold(gray,250,255,cv2.THRESH_BINARY_INV+cv2.THRESH_OTSU)

    _,contours, h = cv2.findContours(thresh, cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
    sort=sorted(contours, key=cv2.contourArea, reverse=True)
    L1=sort[0]

    M1 = cv2.moments(L1)
    cx1 = int(M1['m10']/M1['m00'])
    cy1 = int(M1['m01']/M1['m00'])
    cv2.circle(color_image,(cx1,cy1),2,(255,0,0),4)
                
    actual_position = cx1
    error = set_point  - actual_position
    #integral = error + integral
    derivative = error - previous_error
    #correction = kp*error + ki*integral + kd*derivative
    correction = kp*error + kd*derivative
    #turn = correction / 50
    turn = (correction / 10)/2
    pwm1 = pwm1 - turn
    pwm2 = pwm2 + turn
    if pwm1 > 25:
        pwm1=25
    if pwm2 >25:
        pwm2=25
    if pwm1 <10 :
        pwm1=10
    if pwm2<10:
        pwm2=10
    print(str(turn) + " " + str(pwm1) + " " + str(pwm2) + " "+str(cx1))    
    previous_error = error
    GPIO.output(Motor1A,GPIO.LOW)
    GPIO.output(Motor1B,GPIO.HIGH)
    left.ChangeDutyCycle(pwm1)
    #left.ChangeDutyCycle(20)
    GPIO.output(Motor2A,GPIO.LOW)
    GPIO.output(Motor2B,GPIO.HIGH)
    right.ChangeDutyCycle(pwm2)
    #right.ChangeDutyCycle(20)
    sleep(0.1)
    
    
    cv2.imshow("Video",color_image)
    cv2.imshow("thresh",thresh)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
    raw_cap.truncate(0)

print "Ending...."
GPIO.output(Motor1E,GPIO.LOW)
GPIO.output(Motor2E,GPIO.LOW)
 
GPIO.cleanup()

cv2.destroyAllWindows()
