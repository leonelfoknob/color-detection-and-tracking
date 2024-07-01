import cv2
import numpy as np
import serial
import time

arduino = serial.Serial(port='COM21', baudrate=115200, timeout=1)

cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH,640)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT,480)

_,frame = cap.read()
rows,cols, _ = frame.shape
x_medium = int(cols/2)
y_medium = int(rows/2)

pos_orta = 90
servo_position_x = pos_orta
servo_position_y = 90

center_target_x = int(cols/2)
center_target_y = int(rows/2) 

while True:
    _,frame = cap.read()
    hsv = cv2.cvtColor(frame,cv2.COLOR_BGR2HSV)

    lower_blue = np.array([90,50,50])
    upper_blue = np.array([130,255,255])
    mask_blue =cv2.inRange(hsv,lower_blue,upper_blue)
    blue_color = cv2.bitwise_and(frame,frame,mask=mask_blue)

    contours,_ = cv2.findContours(mask_blue,cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    contours = sorted(contours, key=lambda x:cv2.contourArea(x),reverse=True)

    for cnt in contours:
        (x,y,w,h) = cv2.boundingRect(cnt)
        x_medium = int((x+(x+w))/2)
        y_medium = int((y+(y+h))/2)

        cv2.rectangle(frame,(x,y),(x+w,y+h),(0,255,85),2)
        cv2.circle(frame,(x_medium,y_medium),8,(255,255,0),2)
        if x_medium>280 and x_medium < 320:
            servo_position_x = servo_position_x
            arduino.write(bytes(str(servo_position_x), 'utf-8'))
        elif x_medium < 280:
            servo_position_x = servo_position_x + 1
            if servo_position_x >= 180:
                servo_position_x = 180
                arduino.write(bytes(str(servo_position_x), 'utf-8'))
        elif x_medium > 320:
            servo_position_x = servo_position_x-1
            if servo_position_x <= 0:
                servo_position_x = 0
            arduino.write(bytes(str(servo_position_x), 'utf-8'))
            #make the same thing for y axis
        print(servo_position_x)#send it to command servo
        break

    cv2.line(frame,(x_medium,0),(x_medium,720),(0,85,255),2)
    #cv2.line(frame,(0,y_medium),(1280,y_medium),(0,85,255),2)

    cv2.imshow("frame",frame)
    cv2.imshow("mask_blue",mask_blue)

    if cv2.waitKey(1) == ord('q'):
        break
    #print(x_medium)
    #send value to servo
    
    
    

cap.release()

#https://www.youtube.com/watch?v=Mx-zXDWYWoA&ab_channel=Pysource : link for learn