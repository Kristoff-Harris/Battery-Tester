#-------------------------------------------------------------------------------------------------------------
# File          : deviceconnection.py
# Create Date   : 9/9/2017
# Purpose       : Houses the code which connects to the bank IEEE
#
#-------------------------------------------------------------------------------------------------------------


#import [Library needed for IEEE if not serial]
import serial
import io

#Static definition of COM Ports, maybe more elegant solution is possible in the future. 
Bank1_Port='COM6'
Bank2_Port='COM7'

#Define Serial Aliases 
ser1 = serial.Serial()
ser1.baudrate = 9600
ser1.port = Bank1_Port



ser2 = serial.Serial()
ser2.baudrate = 9600
ser2.port = Bank2_Port

ser1.open()
sio = io.TextIOWrapper(io.BufferedRWPair(ser1, ser1,1),encoding='ascii')
sio.write(str("ID?\n"))

#sio.flush() # it is buffering. required to get the data out *now*
#IDtype = sio.readline()
ser1.close()
IDtype2 = IDtype
#  Ultimately your call but my thought is to return True if we can successfully connect to the Bank IEEE interface and
# False if we cannot
def getBank1ConnStatus():
    ser1.open()
    ser1.write(b'ID?')
    #Checkline = ser1.readline()
    ser1.close()
    return True

def getBank2ConnStatus():
    # TODO  put code to do a healthcheck on Bank2
    return True

def getBank1Voltage():
    return 4

def getBank2Voltage():
    return 6

def getBank1Current():
    return 7

def getBank2Current():
    return 8

def getBank1Load():
    return 10

def getBank2Load():
    return 11

