import serial
import time
arduino = serial.Serial(port='COM21', baudrate=115200, timeout=1)

pos_deg = 0

pos_servo_x = 150
pos_servo_y = 150
#send to Arduino 
def write_read():
    pos_deg = input("aci girin")
    arduino.write(bytes(pos_deg, 'utf-8'))
    time.sleep(1)
    #data = arduino.readline()
    #data = data.decode()
    #return data

while True:
    pos_deg = input("aci girin")
    arduino.write(bytes(pos_deg, 'utf-8'))
    #num = input("Enter a number: ") # Taking input from user
    #x=joystick()
    #print(x)
    #write_read()
    print(pos_deg)
    #value = write_read()
    #print(value) # printing the value