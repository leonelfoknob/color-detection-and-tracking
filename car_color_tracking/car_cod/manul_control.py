import serial.tools.list_ports
import serial
import time


def read_sensor_data():
    data = ser.readline()
    return data.decode()

ports = list(serial.tools.list_ports.comports())
for p in ports:
    print (p)
    if "Arduino" in p.description:
    #if "CH340" in p.description:
        ser = serial.Serial(p[0],115200, timeout=0.1)
        print ("car Succefully connected!")
        while True:
            komut = input("komut gir : ")
            ser.write(bytes(str(komut), 'utf-8'))
            #time.sleep(0.1)
            print(komut)