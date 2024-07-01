import serial.tools.list_ports
import serial
import time
import cv2
import numpy as np

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

komut ="b"
ports = list(serial.tools.list_ports.comports())
for p in ports:
    #print (p)
    if "CH340" in p.description:
        ser = serial.Serial(p[0],115200, timeout=0.001)
        print ("car Succefully connected!")
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

                print(y_medium)
                if y_medium >200 and y_medium < 300:
                    ser.write(bytes("q", 'utf-8'))
                elif y_medium > 300:
                    ser.write(bytes("w", 'utf-8'))
                elif y_medium < 200:
                    ser.write(bytes("s", 'utf-8'))
                else:
                    ser.write(bytes("q", 'utf-8'))
                
                cv2.rectangle(frame,(x,y),(x+w,y+h),(0,255,85),2)
                cv2.circle(frame,(x_medium,y_medium),8,(255,255,0),2)
                break

            #komut = input("komut gir : ")
            #komut = komut.encode('utf-8')
            #ser.write(komut)

            cv2.line(frame,(x_medium,0),(x_medium,720),(0,85,255),2)
            cv2.line(frame,(0,y_medium),(1280,y_medium),(0,85,255),2)
#y limit çizgileri
            cv2.line(frame,(0,200),(1280,200),(0,0,255),2)
            cv2.line(frame,(0,300),(1280,300),(0,0,255),2)

            cv2.imshow("frame",frame)
            cv2.imshow("mask_blue",mask_blue)
            if cv2.waitKey(1) == ord('q'):
                break
cap.release()
ser.write(bytes("q", 'utf-8'))