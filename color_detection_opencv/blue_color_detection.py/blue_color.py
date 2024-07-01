import cv2
import numpy as np
import serial
import time

arduino = serial.Serial(port='COM21', baudrate=115200, timeout=0.1)

cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH,640)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT,480)

x_screen_center = int(640/2)
y_screen_center = int(480/2)

x_detection_limit_left = (x_screen_center-270)
x_detection_limit_right = (x_screen_center+270)
y_detection_limit_up = (y_screen_center-210)
y_detection_limit_down = (y_screen_center+210)

x_target_left = (x_screen_center-100)
x_target_right = (x_screen_center+100)
y_target_up = (y_screen_center-100)
y_target_down = (y_screen_center+100)

command=""
command_byte = ""
angle_motor_x = 90
angle_motor_y = 90

while True:
    ret,frame = cap.read()
    '''width = int(cap.get(3))
    height = int(cap.get(4))'''

    hsv = cv2.cvtColor(frame,cv2.COLOR_BGR2HSV)

    lowe_blue = np.array([90,50,50])
    upper_blue = np.array([130,255,255])
    mask_blue =cv2.inRange(hsv,lowe_blue,upper_blue)
    blue_color = cv2.bitwise_and(frame,frame,mask=mask_blue)

    '''low_red  = np.array([161, 155, 84])
    high_red = np.array([179, 255 ,255])
    red_mask = cv2.inRange(hsv, low_red, high_red)
    red_color = cv2.bitwise_and(frame,frame,mask=red_mask)'''

    contours, _ = cv2.findContours(mask_blue,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
    #contours = sorted(contours, key=lambda x:cv2.contourArea(x), reverse=True)

    for cnt in contours:
        x,y,w,h = cv2.boundingRect(cnt)
        perimeter = cv2.arcLength(cnt, True)
        if perimeter > 300:

            #print(perimeter)

            frame = cv2.drawContours(frame,[cnt],0,(0,255,255),2)
            frame = cv2.rectangle(frame,(x,y),(x+w,y+h),(0,255,0),2)

            rect = cv2.minAreaRect(cnt)
            box = cv2.boxPoints(rect)
            box = np.intp(box)
            frame = cv2.drawContours(frame,[box],0,(0,255,255),2)

            x_medium = int((x + x + w) / 2)
            y_medium = int((y + y + h) / 2)

            frame = cv2.circle(frame,(x_medium,y_medium),5,(255,0,0),2)
            frame = cv2.circle(frame,(x_screen_center,y_screen_center),10,(0,0,255),2)

            frame = cv2.line(frame,(x_screen_center,y_screen_center), (x_medium,y_medium), (0,255,0), 1)

            frame = cv2.line(frame,(x_target_left,0), (x_target_left,480), (0,0,255), 1)
            frame = cv2.line(frame,(x_target_right,0), (x_target_right,480), (0,0,255), 1)
            frame = cv2.line(frame,(0,y_target_down), (640,y_target_down), (0,0,255), 1)
            frame = cv2.line(frame,(0,y_target_up), (640,y_target_up), (0,0,255), 1)

            frame = cv2.line(frame,(x_detection_limit_left,0), (x_detection_limit_left,480), (0,255,0), 1)
            frame = cv2.line(frame,(x_detection_limit_right,0), (x_detection_limit_right,480), (0,255,0), 1)
            frame = cv2.line(frame,(0,y_detection_limit_up), (640,y_detection_limit_up), (0,255,0), 1)
            frame = cv2.line(frame,(0,y_detection_limit_down), (640,y_detection_limit_down), (0,255,0), 1)

            if x_medium < x_detection_limit_right and x_medium > x_detection_limit_left and y_medium > y_detection_limit_up and y_medium <y_detection_limit_down:
                if x_medium < x_target_left and y_medium > y_target_up and y_medium < y_target_down :
                    command = "left"
                    angle_motor_x = angle_motor_x + 1
                    if angle_motor_x >= 180:
                        angle_motor_x = 180
                    command_byte = "l" #left
                    frame= cv2.putText(frame, command + str(angle_motor_x), (50,20), cv2.FONT_HERSHEY_SIMPLEX , 1,(0,0,255), 1, cv2.LINE_AA, False) 
                if x_medium > x_target_right and y_medium > y_target_up and y_medium < y_target_down:
                    command = "right"
                    angle_motor_x = angle_motor_x - 1
                    if angle_motor_x <= 0:
                        angle_motor_x = 0
                    command_byte = "r" #right
                    frame= cv2.putText(frame, command + str(angle_motor_x), (50,20), cv2.FONT_HERSHEY_SIMPLEX , 1,(0,0,255), 1, cv2.LINE_AA, False)
                if y_medium > y_target_down and x_medium < x_target_right and x_medium > x_target_left:
                    command = "bottom"
                    command_byte = "b" #bottom
                    frame= cv2.putText(frame, command, (50,20), cv2.FONT_HERSHEY_SIMPLEX , 1,(0,0,255), 1, cv2.LINE_AA, False)
                if y_medium < y_target_up and x_medium < x_target_right and x_medium > x_target_left:
                    command = "Top"
                    command_byte = "t" #Top
                    frame= cv2.putText(frame, command, (50,20), cv2.FONT_HERSHEY_SIMPLEX , 1,(0,0,255), 1, cv2.LINE_AA, False)
                if x_medium < x_target_right and x_medium > x_target_left and y_medium > y_target_up and y_medium < y_target_down:
                    command = "center"
                    if angle_motor_x > 90:
                        angle_motor_x = angle_motor_x-1
                        if angle_motor_x == 90:
                            angle_motor_x = 90
                    if angle_motor_x < 90:
                        angle_motor_x = angle_motor_x+1
                        if angle_motor_x == 90:
                            angle_motor_x = 90
                    command_byte = "c" #center
                    frame= cv2.putText(frame, command + str(angle_motor_x), (50,20), cv2.FONT_HERSHEY_SIMPLEX , 1,(0,0,255), 1, cv2.LINE_AA, False)
                if x_medium < x_target_left and y_medium < y_target_up:
                    command = "top left"
                    frame= cv2.putText(frame, command, (50,20), cv2.FONT_HERSHEY_SIMPLEX , 1,(0,0,255), 1, cv2.LINE_AA, False)
                if x_medium > x_target_right and y_medium < y_target_up:
                    command = "top right"
                    frame= cv2.putText(frame, command, (50,20), cv2.FONT_HERSHEY_SIMPLEX , 1,(0,0,255), 1, cv2.LINE_AA, False)
                if x_medium < x_target_left and y_medium > y_target_down:
                    command = "bottom left"
                    frame= cv2.putText(frame, command, (50,20), cv2.FONT_HERSHEY_SIMPLEX , 1,(0,0,255), 1, cv2.LINE_AA, False)
                if x_medium > x_target_right and y_medium > y_target_down:
                    command = "bottom right"
                    frame= cv2.putText(frame, command, (50,20), cv2.FONT_HERSHEY_SIMPLEX , 1,(0,0,255), 1, cv2.LINE_AA, False)
            else:
                command = "no target"
                command_byte = "s" #stop
                angle_motor_x = 90
                frame= cv2.putText(frame, command+str(angle_motor_x), (50,20), cv2.FONT_HERSHEY_SIMPLEX , 1,(0,0,255), 1, cv2.LINE_AA, False) 


    cv2.imshow("frame",frame)
    cv2.imshow("HSV",hsv)
    cv2.imshow("mask_blue",mask_blue)
    cv2.imshow("blue_color",blue_color)
    #cv2.imshow("red_color",red_color)
    #print(bytes(str(angle_motor_x), 'utf-8'))
    print(command_byte)
    arduino.write(bytes(command_byte, 'utf-8'))
    
    if cv2.waitKey(1) == ord('q'):
        break

cap.release()