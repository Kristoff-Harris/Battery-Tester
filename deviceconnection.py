#-------------------------------------------------------------------------------------------------------------
# File          : deviceconnection.py
# Create Date   : 9/9/2017
# Purpose       : Houses the code which connects to the bank IEEE
#
#-------------------------------------------------------------------------------------------------------------

import serial
import io
import time
import load_balance as lb
 
setup_complete = False

def setup_serial_ports():
    try:
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
        sio2 = io.TextIOWrapper(io.BufferedRWPair(ser2, ser2,1),encoding='ascii')
        setup_complete = True
    except:
        pass

#  Ultimately your call but my thought is to return True if we can successfully connect to the Bank IEEE interface and
# False if we cannot
def getBank1ConnStatus():
    Checkline = queryTDI_ser1(str("ID?\n"))
    if Checkline[2:-5] == 'WCL 100-1000-12000':
        return True
    else :
        return False

def getBank2ConnStatus():
    Checkline = queryTDI_ser2(str("ID?\n"))

    if Checkline[2:3] == 'W':  #Have to see how the other load bank responds to this request on Telnet (to get more specific)
        return True
    else :
        return False

def getBank1Voltage():
    Checkline = queryTDI_ser1(str("V?\n"))
    lefttext=Checkline.partition(" v")[0]
    return lefttext[2:]
    
    

def getBank2Voltage():
    Checkline = queryTDI_ser2(str("V?\n"))
    lefttext=Checkline.partition(" v")[0]
    return lefttext[2:]

def getBank1Current():
    Checkline = queryTDI_ser1(str("I?\n"))
    lefttext=Checkline.partition(" a")[0]
    return lefttext[2:]

def getBank2Current():
    Checkline = queryTDI_ser2(str("I?\n"))
    lefttext=Checkline.partition(" a")[0]
    return lefttext[2:]

def getBank1Load():
    Checkline = queryTDI_ser1(str("P?\n"))
    lefttext=Checkline.partition(" w")[0]
    return lefttext[2:]

def getBank2Load():
    Checkline = queryTDI_ser2(str("P?\n"))
    lefttext=Checkline.partition(" w")[0]
    return lefttext[2:]

def queryTDI_ser1(write_str):
    try:
        if not setup_complete:
            setup_serial_ports()
        if not ser1.is_open:
            ser1.open()

        sio1.write(write_str)
        sio1.flush() # it is buffering. required to get the data out *now*
        time.sleep(0.05)
        strout = str(ser1.readline())
        ser1.close()
    except:
        strout = ''
    return strout


def queryTDI_ser2(write_str):
    try:
        if not setup_complete:
            setup_serial_ports()
        if not ser2.is_open:
            ser2.open()

        sio2.write(write_str)
        sio2.flush() # it is buffering. required to get the data out *now*
        time.sleep(0.05)
        strout = str(ser2.readline())
        ser2.close()
    except:
        strout = ''
    return strout

def set_TDI_state_ser1(curr,volt,power,mode):
    try:
        if not ser1.is_open:
            ser1.open()
        #Run a switch case on mode to set the value 
        if mode == 1:
            sio1.write(str("CI"+curr+"\n"))
        elif mode == 2:
            sio1.write(str("CV"+volt+"\n"))
        elif mode == 3:
            sio1.write(str("CP"+power+"\n"))
        else:
            pass

        #Write the current command
        sio1.flush() # it is buffering. required to get the data out *now*
        time.sleep(0.05)
        ser1.close()
    except:
        pass
    return 


def set_TDI_state_ser2(curr,volt,power,mode):
    try:
        if not ser1.is_open:
            ser2.open()
        #Run a switch case on mode to set the value 
        if mode == 1:
            sio2.write(str("CI"+curr+"\n"))
        elif mode == 2:
            sio2.write(str("CV"+volt+"\n"))
        elif mode == 3:
            sio2.write(str("CP"+power+"\n"))
        else:
            pass

        #Write the current command
        sio2.flush() # it is buffering. required to get the data out *now*
        time.sleep(0.05)
        ser2.close()
    except:
        pass
    return 

def open_TDI1_contactor():
    try:
        sio1.write(str("LOAD OFF\n"))
    except:
        pass

def open_TDI2_contactor():
    try:
        sio2.write(str("LOAD OFF\n"))
    except:
        pass

def close_TDI1_contactor():
    try:
        sio1.write(str("LOAD ON\n"))
    except:
        pass

def close_TDI2_contactor():
    try:
        sio2.write(str("LOAD ON\n"))
    except:
        pass
