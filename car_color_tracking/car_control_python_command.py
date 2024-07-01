import serial
import time
arduino = serial.Serial(port='COM20', baudrate=115200, timeout=0.1)

#send to Arduino 
def write_read():
    commands = input("command")
    print(commands)
    arduino.write(bytes(str(commands), 'utf-8'))
    time.sleep(0.1)
    #data = arduino.readline()
    #data = data.decode()
    #return data

while True:
    #num = input("Enter a number: ") # Taking input from user
    #x=joystick()
    #print(x)
    write_read()
    #value = write_read()
    #print(value) # printing the value