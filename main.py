from tkinter import *
from tkinter import ttk

# Chris uses this for UI Testing
import dummydeviceconnection as dc
#import deviceconnection as dc


#
#   Create preprogrammed routine variables
#

# We could also make this a more complex data structure and also have time till next command is invoked
routine_1_commands = ['SendV12', 'SendV13', 'SendV14', 'SendV15', 'SendV16']            
# This holds the index to the routine_1_commands
routine_pointer = 0
# This is what will be referenced to check to see if the preprogrammed execution should be continued
preprog_continue = True

def validate_user_value(self, txt):
    print("in the validate_user_value function")
    if not txt:  # Do not accept an empty string
        return False

    try:
        if (int(txt) == True and txt < 100):
            return True  # accept int

    except ValueError:
        return False

def run_preprog_mode():
    # global basically just creates a variable which looks outside of the scope of the function to see if it exists
    # and then sort of "imports" it so we can manipulate it in here and have the changes reflected globally.
    global routine_1_commands
    global routine_pointer

    # Checking to make sure we're still okay to run and we haven't yet hit the end of the command array
    if preprog_continue == True and routine_pointer < len(routine_1_commands):
        print("We should execute " + str(routine_1_commands[routine_pointer]) )
        routine_pointer += 1
        root.after(500, run_preprog_mode)

    #else:
        # Reset the routine pointer
        #routine_pointer = 0


# This code gets called every "Refresh" period, so in it we'll want to check on the status of both banks to make sure theyre
# Online as well as to update the UI values of Bank1 and Bank2

def ui_refresh():
    print("in the poll_sources function")
    print("Current Mode == " + str(mode.get()))
    if(mode.get() == ""):
        print("User has not picked the test bank mode A,B or A&B")

    print("Current Run Param == "+ str(run_param.get()))

    if(run_param.get() == "preprog_selected"):
        print("Pre-Prog Mode == " +  str(predefinedmodevar.get()))


    #initializing the bank variables so if dc.get... command doesn't return anything, they wont be uninitialized
    bank1v = "Unk"
    bank2v = "Unk"
    bank1c = "Unk"
    bank2c = "Unk"
    bank1l = "Unk"
    bank2l = "Unk"

    # Getting the bank 1 and bank 2 values upfront so we don't have to query them multiple times within the ui_refresh method
    bank1v = str(dc.getBank1Voltage())
    bank2v = str(dc.getBank2Voltage())
    bank1c = str(dc.getBank1Current())
    bank2c = str(dc.getBank1Current())
    bank1l = str(dc.getBank1Load())
    bank2l = str(dc.getBank2Load())

    print("Bank1Voltage == " + bank1v)
    print("Bank2Voltage == " + bank2v)
    print("Bank1Current == " + bank1c)
    print("Bank2Current == " + bank2c)
    print("Bank1Load == " + bank1l)
    print("Bank2Load == " + bank2l)

    # Assigning the UI values
    bank_1_current_output_var.set(bank1c)
    bank_1_volt_output_var.set(bank1v)
    bank_1_load_output_var.set(bank1l)
    bank_2_current_output_var.set(bank2c)
    bank_2_volt_output_var.set(bank2v)
    bank_2_load_output_var.set(bank2l)

    # How do we want to handle if the connection to a bank breaks? We should put that code below

    # Doing a basic check to see if a bank is online or offline
    if (dc.getBank1ConnStatus() == True):
        bank_1_heartbeat_var.set("Online")
    else:
        bank_1_heartbeat_var.set("Offline")
    if (dc.getBank2ConnStatus() == True):
        bank_2_heartbeat_var.set("Online")
    else:
        bank_2_heartbeat_var.set("Offline")

    #Check to make sure load bank 1 has not faulted, if so, stop loadbank 2.  ###NEED TO FIX, WORKS ALL THE TIME VERSUS WHEN LB 2 is not requested.....
    loadbank_stat = dc.getBank1Contactor()
    global Contactor_LB1_Status_Old
    if (Contactor_LB1_Status_Old == True) & (loadbank_stat == False):
        onClickStop()
        Contactor_LB1_Status_Old = False
    elif loadbank_stat == True:
        Contactor_LB1_Status_Old = True





    # This is needed to make sure another call to this happens in 5 sec (or .5 sec if 500)
    root.after(500, ui_refresh)


def print_selected():
    print("Combobox changed")

    dc.set_TDI_state_ser1(0, 0, 0, 1)
    dc.set_TDI_state_ser2(0, 0, 0, 1)
    ## Call to zero load
    # State of the combo box will need to be known later but for now we just want to put
    # the load bank in a safe mode


# Fires when someone clicks the "start" button
def onClickStart():
    print("Start Button Pressed")
    current_testing_status.set("Running")

    global preprog_continue

    #invoke the special code for preprog mode
    if (run_param.get() == "preprog_selected"):
        preprog_continue = True
        run_preprog_mode()

    # Set the current to zero amps
    dc.set_TDI_state_ser1(0, 0, 0, 1)
    dc.set_TDI_state_ser2(0, 0, 0, 1)
    # Close both contactors
    dc.close_TDI1_contactor()
    dc.close_TDI2_contactor()
    # If the combobox is set to a script fire that off


# Fires when someone clicks the "stop" button
def onClickStop():
    print("Stop Button Pressed")
    current_testing_status.set("Stopped")

    global preprog_continue
    global routine_pointer

    # Reset the preprogrammed routine
    if (run_param.get() == "preprog_selected"):
        preprog_continue = False
        routine_pointer = 0

    ## Call to zero load
    dc.set_TDI_state_ser1(0, 0, 0, 1)
    dc.set_TDI_state_ser2(0, 0, 0, 1)
    sv.set(0)
    ## Call to open contactor
    dc.open_TDI1_contactor()
    dc.open_TDI2_contactor()


# This checks the value of the user input box for Voltage Current or Power
def validate_float(var):
    print("in the validate_float() function")
    old_value = ''
    new_value = var.get()
    try:
        new_value == '' or float(new_value)
        if (float(new_value) > 1200 and run_param.get() == 'c_selected'):
            print('Current Draw Limits exceeded! Parameter too large!')
            var.set(old_value)
        elif (float(new_value) > 18000 and run_param.get() == 'pow_selected'):
            print('Power Draw Limits exceeded! Parameter too large!')
            var.set(old_value)
        else:
            if run_param.get() == 'c_selected':
                dc.set_TDI_state_ser1(float(new_value), 0, 0, 1)
            elif run_param.get() == 'v_selected':
                dc.set_TDI_state_ser2(0, float(new_value), 0, 2)
            elif run_param.get() == 'pow_selected':
                dc.set_TDI_state_ser2(0, 0, float(new_value), 3)
    except:
        var.set(old_value)


def Script_440A_2_seconds():
    dc.set_TDI_state_ser1(0, 0, 0, 1)
    dc.set_TDI_state_ser2(0, 0, 0, 1)

def fetch():
    print("Input => " + str( run_val.get()))             # get text
    #ent.delete('0', END)
    #run_val.insert(END, 'x')
    #run_val.insert(0, 'x')

root = Tk()
root.title("Battery Testing Application v0.1")
content = ttk.Frame(root, padding=(20,20,12,12))

sv = StringVar()

# trace wants a callback with nearly useless parameters, fixing with lambda.
sv.trace('w', lambda nm, idx, mode, var=sv: validate_float(var))
#sv.trace('w', lambda nm, validate='enter', mode, var=sv: validate_float(var))

global mode
mode = StringVar()

global Contactor_LB1_Status_Old  # Allow hystersis on the diagnosing load bank 1 has faulted (stopping cooling flow)
Contactor_LB1_Status_Old = False

bank_mode_frame = Frame(content, bd=2, relief=SUNKEN, borderwidth=5)
run_mode_frame = Frame(content, bd=2, relief=SUNKEN, borderwidth=5)
preprog_mode_frame = Frame(content, bd=2, relief=SUNKEN, borderwidth=5)

a_option = ttk.Radiobutton(bank_mode_frame, text='Load Bank A (WCL 100-1000-12000)', variable=mode, value='a_only')
#b_option = ttk.Radiobutton(bank_mode_frame, text='Load Bank B (WCL 400-200-6000)', variable=mode, value='b_only')
both_option = ttk.Radiobutton(bank_mode_frame, text='Load Bank A&B (A & WCL 400-200-6000)', variable=mode, value='both')

global run_param
run_param = StringVar()

run_val = ttk.Entry(run_mode_frame, textvariable=sv)

run_val.bind('<Return>', (lambda event: fetch()) )

volt_option = ttk.Radiobutton(run_mode_frame, text='Constant Voltage Setpoint', variable=run_param, value='v_selected')
current_option = ttk.Radiobutton(run_mode_frame, text='Constant Current Mode', variable=run_param, value='c_selected')
power_option = ttk.Radiobutton(run_mode_frame, text='Constant Power Mode', variable=run_param, value='pow_selected')
static_option = ttk.Radiobutton(preprog_mode_frame, text='Use Routine', variable=run_param, value='preprog_selected')

global predefinedmodevar
predefinedmodevar = StringVar()
predef = ttk.Combobox(preprog_mode_frame, textvariable=predefinedmodevar)
predef.bind('<<ComboboxSelected>>', print_selected())
predef['values'] = ('Pre-defined 1', 'Pre-defined 2', 'Pre-defined 3')

###############
#
# Creating UI Elements
#
###############
namelbl = ttk.Label(content, text="Name")
name = ttk.Entry(content)

contact_info = ttk.Label(content, text="Built by Chris and Dan Harris")

input_header = ttk.Label(content, text="SELECT INPUT TYPE", font=18)
testing_status = ttk.Label(content, text="TESTING STATUS: ", font=22)

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



global current_testing_status
current_testing_status = StringVar()
current_testing_status.set("Stopped")
current_testing_status_screenvalue = ttk.Label(content, textvariable=current_testing_status, font=18)


curr_mode_title =  ttk.Label(content, text="Load Bank Selection", font=22)
curr_output_title = ttk.Label(content, text="CURRENT OUTPUT", font=22)
title_style = ttk.Style()
title_style.configure("GO.TButton",  foreground="green", background="green")

heartbeat_frame = Frame(content, bd=2, relief=RAISED, borderwidth=5)

bank_output_frame = Frame(content, bd=2, relief=RAISED, borderwidth=5)

# Creating Text Labels for reach bank value
bank_1_current_output_text = ttk.Label(bank_output_frame, text="B1 Curr:")
bank_1_volt_output_text = ttk.Label(bank_output_frame, text="B1 V: ")
bank_1_load_output_text = ttk.Label(bank_output_frame, text="B1 Power: ")
bank_1_heartbeat_text = ttk.Label(heartbeat_frame, text="B1 Status:")
bank_2_current_output_text = ttk.Label(bank_output_frame, text="B2 Curr:")
bank_2_volt_output_text = ttk.Label(bank_output_frame, text="B2 V:")
bank_2_load_output_text = ttk.Label(bank_output_frame, text="B2 Power:")
bank_2_heartbeat_text = ttk.Label(heartbeat_frame, text="B2 Status:")

# Setting the screenvalue and default value (Seen at startup) of each bank value to be displayed on screen
bank_1_current_output_screenvalue = ttk.Label(bank_output_frame, textvariable=bank_1_current_output_var)
bank_1_current_output_var.set("...")
bank_1_volt_output_screenvalue = ttk.Label(bank_output_frame, textvariable=bank_1_volt_output_var)
bank_1_volt_output_var.set("...")
bank_1_load_output_screenvalue = ttk.Label(bank_output_frame, textvariable=bank_1_load_output_var)
bank_1_load_output_var.set("...")
bank_1_heartbeat_screenvalue = ttk.Label(heartbeat_frame, textvariab=bank_1_heartbeat_var)
bank_1_heartbeat_var.set("Loading...")
bank_2_current_output_screenvalue = ttk.Label(bank_output_frame, textvariable=bank_2_current_output_var)
bank_2_current_output_var.set("...")
bank_2_volt_output_screenvalue = ttk.Label(bank_output_frame, textvariable=bank_2_volt_output_var)
bank_2_volt_output_var.set("...")
bank_2_load_output_screenvalue = ttk.Label(bank_output_frame, textvariable=bank_2_load_output_var)
bank_2_load_output_var.set("...")
bank_2_heartbeat_screenvalue = ttk.Label(heartbeat_frame, textvariab=bank_2_heartbeat_var)
bank_2_heartbeat_var.set("Loading...")

go_style = ttk.Style()
go_style.configure("GO.TButton", foreground="green", background="green")

stop_style = ttk.Style()
stop_style.configure("STOP.TButton", foreground="red", background="red")

#ok = ttk.Button(content, text="Begin Testing", command=onClickStart, style="GO.TButton")
#cancel = ttk.Button(content, text="Stop", command=onClickStop, style="STOP.TButton")



buttons_frame = Frame(content, bd=2, borderwidth=5)

ok = ttk.Button(buttons_frame, text="Begin Testing", command=onClickStart, style="GO.TButton")
cancel = ttk.Button(buttons_frame, text="Stop", command=onClickStop, style="STOP.TButton")

###############
#
# Using Tkinter to populate out the UI in a grid layout
#
###############


testing_status.grid(column=5, row=0,  sticky=W)
current_testing_status_screenvalue.grid(column=6, row=0, sticky=E)

curr_mode_title.grid(column=0, row=0, sticky=W)
a_option.grid(column=0, row=1, sticky=W)
#b_option.grid(column=0, row=2,sticky=W)
both_option.grid(column=0, row=3, sticky=W)
bank_mode_frame.grid(column=0, row=1, sticky=W+E+N+S)


# Populate Bank 1 output screen labels and vals
curr_output_title.grid(column=4, row=0, pady=5, padx=15, sticky=W+E)

bank_1_current_output_text.grid(column=0, row=0, padx=15 , sticky=W)
bank_1_current_output_screenvalue.grid(column=1, row=0)

bank_1_volt_output_text.grid(column=0, row=1, padx=15 , sticky=W)
bank_1_volt_output_screenvalue.grid(column=1, row=1)

bank_1_load_output_text.grid(column=0, row=2,padx=15 , sticky=W)
bank_1_load_output_screenvalue.grid(column=1, row=2)



bank_2_current_output_text.grid(column=3, row=0, padx=15 , sticky=W)
bank_2_current_output_screenvalue.grid(column=4, row=0)
bank_2_volt_output_text.grid(column=3, row=1, padx=15 , sticky=W)
bank_2_volt_output_screenvalue.grid(column=4, row=1)
bank_2_load_output_text.grid(column=3, row=2, padx=15 , sticky=W)
bank_2_load_output_screenvalue.grid(column=4, row=2)


bank_1_heartbeat_text.grid(column=0, row=0, sticky=W)
bank_1_heartbeat_screenvalue.grid(column=1, row=0, sticky=E)

bank_2_heartbeat_text.grid(column=0, row=1, sticky=W)
bank_2_heartbeat_screenvalue.grid(column=1, row=1, sticky=E)

heartbeat_frame.grid(column=5, row=1, columnspan=2, padx=5, pady=5, sticky=W+E+N+S)

bank_output_frame.grid(column=4, row=1, padx=5, pady=5, sticky=W+E+N+S )


run_val.grid(column=1, row=1, sticky=E)
input_header.grid(column=0, row=3, pady=15, sticky=W)
volt_option.grid(column=0, row=1, sticky=W)
current_option.grid(column=0, row=2, sticky=W)
power_option.grid(column=0, row=3, sticky=W)
static_option.grid(column=0, row=4, sticky=W)
predef.grid(column=1, row=4, columnspan=2)
run_mode_frame.grid(column=0, row=5, sticky=N+S+E+W)
preprog_mode_frame.grid(column=0, row=6)



#ok.grid(column=8, row=6, sticky=N+S+E+W)
#cancel.grid(column=8, row=7,  sticky=N+S+E+W)

ok.grid(column=0, row=0, columnspan=3,  sticky=N+S+E+W)
cancel.grid(column=0, row=1, columnspan=3, sticky=N+S+E+W)
buttons_frame.grid(column=4, row=5,  columnspan=3, sticky=N+S+E+W)

content.grid(column=0, row=0)

contact_info.grid(column=5, row=9, columnspan=3, sticky=E)

###############
#
# Think of this as the MAIN
#
###############

# Kick off the initial refresh sequence - lower to equal 500 to do it every .5 sec
root.after(500, ui_refresh)

root.mainloop()
