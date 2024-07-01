import cv2

cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH,1280)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT,720)

while True:
    _,frame = cap.read()
    hsv_frame = cv2.cvtColor(frame,cv2.COLOR_BGR2HSV)
    height,width,_ = frame.shape

    cx= int(width/2)
    cy = int(height/2)

    pixel_center = hsv_frame[cy,cx]
    hue_value = pixel_center[0]

    color = "undefined"

    if hue_value <5 :
        color = "RED"
    elif hue_value < 22:
        color = "ORANGE"
    elif hue_value < 33:
        color = "YELLOW"
    elif hue_value < 78:
        color = "GREEN"
    elif hue_value <131:
        color = "BLUE"
    elif hue_value < 170:
        color = "VIOLET"
    else:
        color = "RED"

    pixel_center_bgr = frame[cy,cx]
    b,g,r = int(pixel_center_bgr[0]),int(pixel_center_bgr[1]),int(pixel_center_bgr[2])

    cv2.putText(frame,color,(10,50),0,1,(b,g,r),2)
    cv2.circle(frame,(cx,cy),80,(b,g,r),3)
    #print(pixel_center)

    cv2.imshow("frame",frame)

    if cv2.waitKey(1) == ord('q'):
        break

cap.release()