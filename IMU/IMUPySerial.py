import serial

ser = serial.Serial('COM3',baudrate = 115200, timeout = 1 )

while 1:
    data = ser.readline()
    print(data)