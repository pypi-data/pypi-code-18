import serial

def read():
    port = "COM20"
    ser = serial.Serial(port, 9600)
    while True:
        print(ser.readline())

def Cserial_test():
    print('Cserial working')
    