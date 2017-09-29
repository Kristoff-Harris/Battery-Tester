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


global setup_complete
setup_complete = False

def setup_serial_ports():
    global setup_complete
    global ser1
    global ser2
    global sio1
    global sio2
    setup_complete_a = False
    try:
        #Static definition of COM Ports, maybe more elegant solution is possible in the future. 
        Bank1_Port='COM9' # This is the port of the WCL232 100-1000-12000

        #Define Serial Aliases 
        ser1 = serial.Serial()
        ser1.baudrate = 9600
        ser1.port = Bank1_Port
        ser1.timeout = 1
        ser1.open()
        sio1 = io.TextIOWrapper(io.BufferedRWPair(ser1, ser1,1),encoding='ascii')
        setup_complete_a = True
        
    # Dan, If you're interested in seeing what the exception was, use this syntax. It may be helpful for debugging
    except Exception as e:
        print(e)
        pass

    try: 
        Bank2_Port='COM8'  #This is the port of the WCL488 400-200-6000
        ser2 = serial.Serial()
        ser2.baudrate = 9600
        ser2.port = Bank2_Port
        ser2.timeout = 1
        ser2.open()
        sio2 = io.TextIOWrapper(io.BufferedRWPair(ser2, ser2,1),encoding='ascii')
        if setup_complete_a == True: #If A also made it, we are done, setup is complete
            setup_complete = True

    # Dan, If you're interested in seeing what the exception was, use this syntax. It may be helpful for debugging
    except Exception as e:
        print(e)
        pass

#  Ultimately your call but my thought is to return True if we can successfully connect to the Bank IEEE interface and
# False if we cannot
def getBank1ConnStatus():
    try:
        Checkline = queryTDI_ser1(str("ID?\n"))
        if Checkline[0:-1] == 'WCL 100-1000-12000':
            return True
        else :
            return False
    except:
        return False
def getBank2ConnStatus():
    try:
        Checkline = queryTDI_ser2(str("ID?\n"))
        if Checkline[0:-1] == 'WCL 400-200-6000':
            return True
        else :
            return False
    except:
        return False
    

def getBank1Voltage():
    try:
        Checkline = queryTDI_ser1(str("CV?\n"))
        lefttext=Checkline.partition(" v")[0]
        return float(lefttext)
    except:
        return str("Waiting")
    

def getBank2Voltage():
    try:
        Checkline = queryTDI_ser2(str("CV?\n"))
        lefttext=Checkline.partition(" v")[0]
        return float(lefttext)
    except:
        return str("Waiting")

def getBank1Current():
    try:
        Checkline = queryTDI_ser1(str("CI?\n"))
        lefttext=Checkline.partition(" a")[0]
        return float(lefttext)
    except:
        return str("Waiting")

def getBank2Current():
    try:
        Checkline = queryTDI_ser2(str("CI?\n"))
        lefttext=Checkline.partition(" amp")[0]
        return float(lefttext)
    except:
        return str("Waiting")


def getBank1Load():
    try:
        Checkline = queryTDI_ser1(str("P?\n"))
        lefttext=Checkline.partition(" w")[0]
        return float(lefttext[2:])
    except:
        return str("Waiting")


def getBank2Load():
    try:
        Checkline = queryTDI_ser2(str("P?\n"))
        lefttext=Checkline.partition(" w")[0]
        return float(lefttext[2:])
    except:
        return str("Waiting")


def getBank1Contactor():
    try:
        Checkline = queryTDI_ser1(str("LOAD?\n"))
        lefttext=Checkline.partition(" \\")[0]
        righttext=Checkline.partition("LOAD ")[2]

        if str(righttext[1]) == "N":  #N: N is for ON
            status_Load1 = True
        else:
            status_Load1 = False

        return status_Load1
    except:
        return False

def getBank2Contactor():
    try:
        Checkline = queryTDI_ser2(str("LOAD?\n"))
        lefttext=Checkline.partition(" \\")[0]
        righttext=Checkline.partition("LOAD ")[2]

        if str(righttext[1]) == "N":  #N: N is for ON
            status_Load2 = True
        else:
            status_Load2 = False

        return status_Load2
    except:
        return False

def queryTDI_ser1(write_str):
    try:
        global setup_complete
        if not setup_complete:
            setup_serial_ports()
        if not ser1.is_open == True:
            ser1.open()

        sio1.flush()
        ser1.flush()
        time.sleep(0.3)
        sio1.write(write_str)
        time.sleep(0.3)
        sio1.flush() # it is buffering. required to get the data out *now*
        #ser1.flush()
        #time.sleep(0.1)
        strout = str(sio1.readline())
        #ser1.close()
    except:
        strout = ''
    return strout


def queryTDI_ser2(write_str):
    try:
        if not setup_complete == True:
            setup_serial_ports()
        if not ser2.is_open:
            ser2.open()

        sio2.flush()
        #ser2.flush()
        time.sleep(0.3)
        sio2.write(write_str)
        time.sleep(0.3)
        strout = str(sio2.readline())
        #ser2.close()
    except:
        strout = ''
    return strout

def set_TDI_state_ser1(curr,volt,power,LB_mode,Test_mode):
    try:
        if not ser1.is_open:
            ser1.open()
        #ser1.reset_output_buffer()
        #ser1.reset_input_buffer()
            #Run a switch case on LB_mode to set the value 
        if LB_mode == 1:
            current_request = lb.factor1(curr,Test_mode)
            range_request = lb.range1(current_request)
            #write_str = (str("RNG ") + str(range_request) +str("\n") + str("CI ") + str(current_request) + str("\n"))
            write_str = (str("CI ") + str(current_request)[:5] + str("\n"))
        elif LB_mode == 2:
            #sio2.write(str("CV "+volt+"\n"))
            write_str = (str("CV ")+ str(volt) + str("\n"))
        elif LB_mode == 3:
            #sio2.write(str("CP "+power+"\n"))
            write_str = (str("CP ")+ str(power) + str("\n"))
        else:
            pass
        sio1.flush() #
        ser1.flush()
        sio1.write(write_str)
        time.sleep(0.1)
        #Write the current command
       #sio1.write(write_str) # it is buffering. required to get the data out *now*
        sio1.flush()
        #ser1.flush()
        strout = str(sio1.readline())
        #strout = str(sio1.readline())

        #time.sleep(0.2)
        #ser1.close()
    except:
        pass
    return 


def set_TDI_state_ser2(curr,volt,power,LB_mode,Test_mode):
    try:
        if not ser2.is_open:
            ser2.open()
        #ser2.reset_output_buffer()
        #ser2.reset_input_buffer()
            #Run a switch case on LB_mode to set the value 
        if LB_mode == 1:
            current_request = lb.factor2(curr,Test_mode)
            range_request = lb.range2(current_request)
            #write_str = (str("RNG ") + str(range_request) +str("\n") + str("CI ") + str(current_request) + str("\n"))
            write_str = (str("CI ") + str(current_request)[:5]  + str("\n"))
        elif LB_mode == 2:
            #sio2.write(str("CV "+volt+"\n"))
            write_str = (str("CV ")+ str(volt) + str("\n"))
        elif LB_mode == 3:
            #sio2.write(str("CP "+power+"\n"))
            write_str = (str("CP ")+ str(power) + str("\n"))
        else:
            pass
        sio2.flush()
        ser2.flush()
        sio2.write(write_str)
        time.sleep(0.1)
        #Write the current command
        sio2.flush() # it is buffering. required to get the data out *now*
        #sio2.flush() # it is buffering. required to get the data out *now*
        strout = str(sio2.readline())
        #strout = str(sio2.readline())
        #time.sleep(0.05)
        #ser2.close()
    except:
        pass
    return 

def open_TDI1_contactor():
    try:
        sio1.write(str("LOAD OFF\n"))
        sio1.flush()
        time.sleep(0.1)
        strout = str(sio1.readline())
    except:
        pass

def open_TDI2_contactor():
    try:
        sio2.write(str("LOAD OFF\n"))
        sio2.flush()
        time.sleep(0.2)
        strout = str(sio2.readline())
    except:
        pass

def close_TDI1_contactor():
    try:
        sio1.write(str("LOAD ON\n"))
        sio1.flush()
        time.sleep(0.1)
        strout = str(sio1.readline())
    except:
        pass

def close_TDI2_contactor():
    try:
        sio2.write(str("LOAD ON\n"))
        sio2.flush()
        time.sleep(0.1)
        strout = str(sio2.readline())
    except:
        pass

def close_conn():
    try:
        ser1.close()
    except:
        pass
    try:
        ser2.close()
    except:
        pass

