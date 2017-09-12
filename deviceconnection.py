#-------------------------------------------------------------------------------------------------------------
# File          : deviceconnection.py
# Create Date   : 9/9/2017
# Purpose       : Houses the code which connects to the bank IEEE
#
#-------------------------------------------------------------------------------------------------------------


#import [Library needed for IEEE if not serial]
import serial
import io
import time
 
#Static definition of COM Ports, maybe more elegant solution is possible in the future. 
Bank1_Port='COM8' # This is the port of the WCL232 100-1000-12000
Bank2_Port='COM7'

#Define Serial Aliases 
ser1 = serial.Serial()
ser1.baudrate = 9600
ser1.port = Bank1_Port
ser1.timeout = 1



ser2 = serial.Serial()
ser2.baudrate = 9600
ser2.port = Bank2_Port
ser2.timeout = 1

sio1 = io.TextIOWrapper(io.BufferedRWPair(ser1, ser1,1),encoding='ascii')


#  Ultimately your call but my thought is to return True if we can successfully connect to the Bank IEEE interface and
# False if we cannot
def getBank1ConnStatus():
    ser1.open()
    sio1.write(str("ID?\n"))
    sio1.flush() # it is buffering. required to get the data out *now*
    time.sleep(0.05)
    Checkline = str(ser1.readline())
    ser1.close()
    if Checkline[2:-5] == 'WCL 100-1000-12000':
        return True
    else :
        return False

def getBank2ConnStatus():
    # TODO  put code to do a healthcheck on Bank2
    return False

def getBank1Voltage():
    ser1.open()
    sio1.write(str("V?\n"))
    sio1.flush() # it is buffering. required to get the data out *now*
    time.sleep(0.05)
    Checkline = str(ser1.readline())
    ser1.close()
   
    lefttext=Checkline.partition(" v")[0]
    return lefttext[2:]
    
    

def getBank2Voltage():
    return 6

def getBank1Current():
    ser1.open()
    sio1.write(str("I?\n"))
    sio1.flush() # it is buffering. required to get the data out *now*
    time.sleep(0.05)
    Checkline = str(ser1.readline())
    ser1.close()
   
    lefttext=Checkline.partition(" a")[0]
    return lefttext[2:]

def getBank2Current():
    return 8

def getBank1Load():
    ser1.open()
    sio1.write(str("P?\n"))
    sio1.flush() # it is buffering. required to get the data out *now*
    time.sleep(0.05)
    Checkline = str(ser1.readline())
    ser1.close()
   
    lefttext=Checkline.partition(" w")[0]
    return lefttext[2:]

def getBank2Load():
    return 11

