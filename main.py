
from tkinter import *
from tkinter import ttk
import deviceconnection as dc


def validate_user_value(self,txt):
    print("in the validate_user_value function")
    if not txt:     # Do not accept an empty string
        return False

    try:
        if(int(txt) == True and txt < 100):
            return True    # accept int

    except ValueError:
        return False


# This code gets called every "Refresh" period, so in it we'll want to check on the status of both banks to make sure theyre
# Online as well as to update the UI values of Bank1 and Bank2

def ui_refresh():
    print("in the poll_sources function")
    print("Bank1Voltage == " + str(dc.getBank1Voltage()))
    print("Bank2Voltage == " + str(dc.getBank2Voltage()))
    print("Bank1Current == " + str(dc.getBank1Current()))
    print("Bank2Current == " + str(dc.getBank2Current()))
    print("Bank1Load == " + str(dc.getBank1Load()))
    print("Bank2Load == " + str(dc.getBank2Load()))

    # Assigning the UI values
    bank_1_current_output_var.set("1")
    bank_1_volt_output_var.set("2")
    bank_1_load_output_var.set("3")
    bank_2_current_output_var.set("4")
    bank_2_volt_output_var.set("5")
    bank_2_load_output_var.set("6")

    #How do we want to handle if the connection to a bank breaks? We should put that code below

    # Doing a basic check to see if a bank is online or offline
    if(dc.getBank1ConnStatus() == True):
        bank_1_heartbeat_var.set("Online")
    else:
        bank_1_heartbeat_var.set("Offline")
    if (dc.getBank2ConnStatus() == True):
        bank_2_heartbeat_var.set("Online")
    else:
        bank_2_heartbeat_var.set("Offline")


    #This is needed to make sure another call to this happens in 5 sec (or .5 sec if 500)
    root.after(5000, ui_refresh)

   


def print_selected():
    print("Combobox changed")

    set_TDI_state_ser1(0,0,0,1)
    ## Call to zero load
    # State of the combo box will need to be known later but for now we just want to put
    # the load bank in a safe mode

# Fires when someone clicks the "start" button
def onClickStart():
    print("Start Button Pressed")

# Fires when someone clicks the "stop" button
def onClickStop():
    print("Stop Button Pressed")
    ## Call to zero load
    ## Call to open contactor


# This checks the value of the user input box for Voltage Current or Power
def validate_float(var):
    print("in the validate_float() function")
    old_value = ''
    new_value = var.get()
    try:
        new_value == '' or float(new_value)
        if float(new_value) > 100:
            print('Input limit exceeded! Parameter too large!')
            var.set(old_value)

    except:
        var.set(old_value)


root = Tk()
root.title("Battery Testing Application v0.1")
content = ttk.Frame(root)

sv = StringVar()

# trace wants a callback with nearly useless parameters, fixing with lambda.
sv.trace('w', lambda nm, idx, mode, var=sv: validate_float(var))

mode = StringVar()
simul_option = ttk.Radiobutton(content, text='Test Banks Simul', variable=mode, value='simul')
individ_option = ttk.Radiobutton(content, text='Test Banks Indiv', variable=mode, value='individual')

run_param = StringVar()


run_val = ttk.Entry(content, textvariable=sv)
volt_option = ttk.Radiobutton(content, text='V Input', variable=run_param, value='v_selected')
current_option = ttk.Radiobutton(content, text='C Input', variable=run_param, value='c_selected')
power_option = ttk.Radiobutton(content, text='Pow Input', variable=run_param, value='pow_selected')
static_option = ttk.Radiobutton(content, text='Use PreProg', variable=run_param, value='preprog_selected')


predefinedmodevar = StringVar()
predef = ttk.Combobox(content, textvariable=predefinedmodevar)
predef.bind('<<ComboboxSelected>>', print_selected())
predef['values'] = ('Pre-defined 1', 'Pre-defined 2', 'Pre-defined 3')


###############
#
# Creating UI Elements
#
###############
namelbl = ttk.Label(content, text="Name")
name = ttk.Entry(content)

contact_info = ttk.Label(content, text="Built by Dan Harris")

input_header = ttk.Label(content, text="SELECT INPUT TYPE")
testing_status = ttk.Label(content, text="TESTING STATUS: INACTIVE ")

# Making these all global so they can be assigned in the refresh routine without needing pass by reference
global bank_1_current_output_var
bank_1_current_output_var = StringVar()

global bank_1_volt_output_var
bank_1_volt_output_var = StringVar()

global bank_1_load_output_var
bank_1_load_output_var = StringVar()

global bank_1_heartbeat_var
bank_1_heartbeat_var = StringVar()

global bank_2_current_output_var
bank_2_current_output_var = StringVar()

global bank_2_volt_output_var
bank_2_volt_output_var = StringVar()

global bank_2_load_output_var
bank_2_load_output_var = StringVar()

global bank_2_heartbeat_var
bank_2_heartbeat_var = StringVar()

#Creating Text Labels for reach bank value
bank_1_current_output_text = ttk.Label(content, text="B1 Curr:")
bank_1_volt_output_text = ttk.Label(content, text="B1 V: ")
bank_1_load_output_text = ttk.Label(content, text="B1 Load: ")
bank_1_heartbeat_text = ttk.Label(content, text="B1 Status:")
bank_2_current_output_text = ttk.Label(content, text="B2 Curr:")
bank_2_volt_output_text = ttk.Label(content, text="B2 V:")
bank_2_load_output_text = ttk.Label(content, text="B2 Load:")
bank_2_heartbeat_text = ttk.Label(content, text="B2 Status:")

# Setting the screenvalue and default value (Seen at startup) of each bank value to be displayed on screen
bank_1_current_output_screenvalue = ttk.Label(content, textvariable = bank_1_current_output_var)
bank_1_current_output_var.set("...")
bank_1_volt_output_screenvalue = ttk.Label(content, textvariable = bank_1_volt_output_var)
bank_1_volt_output_var.set("...")
bank_1_load_output_screenvalue = ttk.Label(content, textvariable = bank_1_load_output_var)
bank_1_load_output_var.set("...")
bank_1_heartbeat_screenvalue = ttk.Label(content, textvariab = bank_1_heartbeat_var)
bank_1_heartbeat_var.set("Loading...")
bank_2_current_output_screenvalue = ttk.Label(content, textvariable = bank_2_current_output_var)
bank_2_current_output_var.set("...")
bank_2_volt_output_screenvalue = ttk.Label(content, textvariable = bank_2_volt_output_var)
bank_2_volt_output_var.set("...")
bank_2_load_output_screenvalue = ttk.Label(content, textvariable = bank_2_load_output_var)
bank_2_load_output_var.set("...")
bank_2_heartbeat_screenvalue = ttk.Label(content, textvariab = bank_2_heartbeat_var)
bank_2_heartbeat_var.set("Loading...")


ok = ttk.Button(content, text="Begin Testing", command=onClickStart)
cancel = ttk.Button(content, text="Stop", command=onClickStop)

###############
#
# Using Tkinter to populate out the UI in a grid layout
#
###############

testing_status.grid(column=7, row=0)
simul_option.grid(column=0, row=1)
individ_option.grid(column=0, row=2)

# Populate Bank 1 output screen labels and vals
bank_1_current_output_text.grid(column=2, row=1)
bank_1_current_output_screenvalue.grid(column=3, row=1)

bank_1_volt_output_text.grid(column=2, row=2)
bank_1_volt_output_screenvalue.grid(column=3, row=2)

bank_1_load_output_text.grid(column=2, row=3)
bank_1_load_output_screenvalue.grid(column=3, row=3)

bank_1_heartbeat_text.grid(column=7, row=1)
bank_1_heartbeat_screenvalue.grid(column=8, row=1)


bank_2_current_output_text.grid(column=4, row=1)
bank_2_current_output_screenvalue.grid(column=5, row=1)
bank_2_volt_output_text.grid(column=4, row=2)
bank_2_volt_output_screenvalue.grid(column=5, row=2)
bank_2_load_output_text.grid(column=4, row=3)
bank_2_load_output_screenvalue.grid(column=5, row=3)
bank_2_heartbeat_text.grid(column=7, row=2)
bank_2_heartbeat_screenvalue.grid(column=8, row=2)


run_val.grid(column=6, row=5)
input_header.grid(column=4, row=4)
volt_option.grid(column=4, row=5)
current_option.grid(column=4, row=6)
power_option.grid(column=4, row=7)
static_option.grid(column=4, row=8)

ok.grid(column=7, row=5)
cancel.grid(column=7, row=6)

content.grid(column=0, row=0)
predef.grid(column=5, row=8, columnspan=2)
contact_info.grid(column=6, row=9, columnspan=3)

###############
#
# Think of this as the MAIN
#
###############

# Kick off the initial refresh sequence - lower to equal 500 to do it every .5 sec
root.after(5000, ui_refresh)

root.mainloop()
