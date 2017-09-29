"""
This function determines a mutiplier to apply to the load command to achieve the 
desired current setpoint and adjusts the feedback to correct for calibration errors.
"""


def factor1(curr, test_mode):
    if test_mode == 2 :
        return curr*0.7 # Dual LB calibration curve goes here 
    elif test_mode == 1 :
        return curr # Single LB calibration curve goes here 
    else:
        return 0

def factor2(curr, test_mode):
    if test_mode == 2 :
        return curr*0.3 # Dual LB calibration curve goes here 
    elif test_mode == 3 :
        return curr # Single LB calibration curve goes here 
    else:
        return 0

def range1(curr):
    #For this application only using one range
    return 5 #50V / 500A

def range2(curr):
    #For this application only using one range
    return 2 #200V 200A
###Reminder, need to set the load bank range!
"""
RNG  x  Set the range (1-9) 
 
(just a reminder)
Range Voltage Current 1 HI HI 2 MED HI 3 LOW HI 4 HI MED 5 MED MED 6 LOW MED 7 HI LOW 8 MED LOW 9 LOW LOW 
"""

#def multiplier_A(Current_SP):
