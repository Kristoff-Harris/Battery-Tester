from tkinter import *
from tkinter import ttk
from threading import Thread


import deviceconnection as dc

#
#   Create preprogrammed routine variables
#

# We could also make this a more complex data structure and also have time till next command is invoked
routine_1_commands = ['StepV12', 'StepV13', 'StepV14', 'StepV15', 'StepV16']
routine_1_durations = [1000, 20000, 5000, 2000, 5000]
rountine_1_curr = [0, 320, 0, 440, 0]


bank1v = ""
bank2v = ""
bank1c = ""
bank2c = ""
bank1l = "Unk"
bank2l = "Unk"



# This holds the index to the routine_1_commands
routine_pointer = 0
# This is what will be referenced to check to see if the preprogrammed execution should be continued
preprog_continue = True

global loadbank1_contact_stat
loadbank1_contact_stat = False

global loadbank2_contact_stat
loadbank2_contact_stat=False

global loadbank1_connect_stat
loadbank1_connect_stat = False

global loadbank2_connect_stat
loadbank2_connect_stat = False

global loadbank_test_config #0 for null #1 for A #2 for both #3 for B
loadbank_test_config = 0

global contactor1_SP
global contactor2_SP
contactor1_SP = False
contactor2_SP = False

global  setpoint1
setpoint1 = [0, 0, 0, 1, loadbank_test_config]

global  setpoint2
setpoint2 = [0, 0, 0, 1, loadbank_test_config]

def validate_user_value(self, txt):
    #print("in the validate_user_value function")
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
    global preprog_continue
    global routine_1_durations
    global rountine_1_curr
    global contactor1
    global contactor2
    global setpoint1
    global setpoint2

    test_indx=predef.get()[0] #Get the first character of the script name, this is the indx of the test to be run.


    # Checking to make sure we're still okay to run and we haven't yet hit the end of the command array
    if preprog_continue == True and routine_pointer < len(routine_1_commands):
        print("Excuting: " + str(routine_1_commands[routine_pointer]))
        Step_duration = routine_1_durations[routine_pointer]
        print("This point is " + str(rountine_1_curr[routine_pointer]) + " Amps for " + str(
            0.001 * Step_duration) + " seconds")
        setpoint2 = [rountine_1_curr[routine_pointer], 0, 0, 1, loadbank_test_config]
        setpoint1 = [rountine_1_curr[routine_pointer], 0, 0, 1, loadbank_test_config]
        routine_pointer += 1
        root.after(Step_duration, run_preprog_mode)
    elif preprog_continue == True:  # The script should have ended correctly
        current_testing_status.set("Script Done")
    else:
        # Reset the routine pointer
        routine_pointer = 0
        preprog_continue = False
        contactor1 = False
        contactor2 = False



def threaded_retriever_function_a():
    try:
 
        global setpoint1
        global loadbank1_connect_stat
        
        if loadbank1_connect_stat == False:
            loadbank1_connect_stat = dc.getBank1ConnStatus()

        #global bank1v
        #bank1v = str(dc.getBank1Voltage())

        #global bank2v
        #bank2v = str(dc.getBank2Voltage())

        global bank1c
        #bank1c = str(dc.getBank1Current())

        #global bank2c
        #bank2c = str(dc.getBank2Current())

        global bank1l
        #bank1l = str(dc.getBank1Load())
        #bank1l = str(setpoint1[0])

        #global bank2l
        #bank2l = str(dc.getBank2Load())

        global loadbank1_contact_stat
        loadbank1_contact_stat = dc.getBank1Contactor()

        global contactor1_SP

        if (contactor1_SP == True) and (loadbank1_contact_stat == False) :
            dc.close_TDI1_contactor()
        elif (contactor1_SP == False) and (loadbank1_contact_stat == True) :
            dc.open_TDI1_contactor()



        bank1l = dc.set_TDI_state_ser1(setpoint1[0],setpoint1[1],setpoint1[2],setpoint1[3],setpoint1[4])

    except Exception as e:
        print(e)
        pass

 
    #print("thread a finished...exiting")


def threaded_retriever_function_b():
    try:


        global setpoint2

        
        global loadbank2_connect_stat
        if loadbank2_connect_stat == False:
            loadbank2_connect_stat = dc.getBank2ConnStatus()

        #global bank1v
        #bank1v = str(dc.getBank1Voltage())

        #global bank2v
        #bank2v = str(dc.getBank2Voltage())

        #global bank1c
        #bank1c = str(dc.getBank1Current())

        #global bank2c
        #bank2c = str(dc.getBank2Current())

        #global bank1l
        #bank1l = str(dc.getBank1Load())

        global bank2l
        #bank2l = str(dc.getBank2Load())
        #bank2l = str(setpoint2[0])

        #global loadbank1_contact_stat
        global loadbank2_contact_stat
        #loadbank1_contact_stat = dc.getBank1Contactor()
        loadbank2_contact_stat = dc.getBank2Contactor()

        #global contactor1_SP
        global contactor2_SP

        #if (contactor1_SP == True) and (loadbank1_contact_stat == False) :
        #    dc.close_TDI1_contactor()
       # elif (contactor1_SP == False) and (loadbank1_contact_stat == True) :
       #     dc.open_TDI1_contactor()

        if (contactor2_SP == True) and (loadbank2_contact_stat == False) :
            dc.close_TDI2_contactor()
        elif (contactor2_SP == False) and (loadbank2_contact_stat == True) :
            dc.open_TDI2_contactor()


        #global setpoint1

        #dc.set_TDI_state_ser1(setpoint1[0],setpoint1[1],setpoint1[2],setpoint1[3],setpoint1[4])
        bank2l = dc.set_TDI_state_ser2(setpoint2[0],setpoint2[1],setpoint2[2],setpoint2[3],setpoint2[4])
    except Exception as e:
        print(e)
        pass

 
    #print("thread b finished...exiting")

# This code gets called every "Refresh" period, so in it we'll want to check on the status of both banks to make sure theyre
# Online as well as to update the UI values of Bank1 and Bank2

def ui_refresh():
    global setpoint1
    global setpoint2

    global loadbank_test_config
    #print("in the poll_sources function")
    #print("Current Mode == " + str(mode.get()))
    if (mode.get() == ""):
        #print("User has not picked the test bank mode A,B or A&B")
        #print("User has not picked the test bank mode A,B or A&B")
        loadbank_test_config=0
    elif mode.get() == "a_only":
        loadbank_test_config=1
    elif mode.get() == "both":
        loadbank_test_config=2
    elif mode.get() == "b_only":
        loadbank_test_config=3
    else:
        loadbank_test_config=0

    #print("Current Run Param == " + str(run_param.get()))

    #if (run_param.get() == "preprog_selected"):
        #print("Pre-Prog Mode == " + str(predefinedmodevar.get()))
    """
    # initializing the bank variables so if dc.get... command doesn't return anything, they wont be uninitialized
    global thread
    # Instantiating a thread object and kicking it off
    if thread.isAlive() == False:
        print("New Thread")
        thread = Thread(target=threaded_retriever_function)
        thread.start()
    """

    global thread_a
    # Instantiating a thread object and kicking it off
    if thread_a.isAlive() == False:
        #print("New Thread_a")
        thread_a = Thread(target=threaded_retriever_function_a)
        thread_a.start()

    global thread_b
    # Instantiating a thread object and kicking it off
    if thread_b.isAlive() == False:
        #print("New Thread_b")
        thread_b = Thread(target=threaded_retriever_function_b)
        thread_b.start()


    #You could add back the join below if you ever wanted to wait for the thread to finish before proceeding
    #thread.join()
    #print("thread finished...exiting")
    #threaded_retriever_function()
    # Getting the bank 1 and bank 2 values upfront so we don't have to query them multiple times within the ui_refresh method
    """
    # For the code below to be more accurate when it's printed, it should be moved into the thread
    print("Bank1Voltage == " + bank1v)
    print("Bank2Voltage == " + bank2v)
    print("Bank1Current == " + bank1c)
    print("Bank2Current == " + bank2c)
    print("Bank1Load == " + bank1l)
    print("Bank2Load == " + bank2l)
    """
    # Assigning the UI values
    bank_1_current_output_var.set(bank1c)
    bank_1_volt_output_var.set(bank1v)
    bank_1_load_output_var.set(bank1l)
    bank_2_current_output_var.set(bank2c)
    bank_2_volt_output_var.set(bank2v)
    bank_2_load_output_var.set(bank2l)

    # How do we want to handle if the connection to a bank breaks? We should put that code below



    # Check to make sure load bank 1 has not faulted, if so, stop loadbank 2.

    global Contactor_LB1_Status_Old
    if (Contactor_LB1_Status_Old == True) & (loadbank1_contact_stat == False):
        onClickStop()
        Contactor_LB1_Status_Old = False
    elif loadbank1_contact_stat == True:
        Contactor_LB1_Status_Old = True

    if loadbank1_contact_stat == True:
        loadbank1_contact_stat_str = 'Contactor Closed'
    else:
        loadbank1_contact_stat_str = 'Contactor Open'

    if loadbank2_contact_stat == True:
        loadbank2_contact_stat_str = 'Contactor Closed'
    else:
        loadbank2_contact_stat_str = 'Contactor Open'
    global loadbank1_connect_stat
    global loadbank2_connect_stat
    # Doing a basic check to see if a bank is online or offline
    if (loadbank1_connect_stat == True):
        bank_1_heartbeat_var.set("Online: " + loadbank1_contact_stat_str)
    else:
        bank_1_heartbeat_var.set("Offline ")
    if (loadbank1_connect_stat == True):
        bank_2_heartbeat_var.set("Online: " + loadbank2_contact_stat_str)
    else:
        bank_2_heartbeat_var.set("Offline ")

    # This is needed to make sure another call to this happens in 5 sec (or .5 sec if 500)
    root.after(250, ui_refresh)


def print_selected():
    #print("Combobox changed")
    preprog_continue = False
    global setpoint1
    global setpoint2

    #setpoint1 = [0, 0, 0, 1, loadbank_test_config]
    #setpoint2 = [0, 0, 0, 1, loadbank_test_config]
    #dc.set_TDI_state_ser1(0, 0, 0, 1, mode.get())
    #dc.set_TDI_state_ser2(0, 0, 0, 1, mode.get())
    ## Call to zero load
    # State of the combo box will need to be known later but for now we just want to put
    # the load bank in a safe mode


# Fires when someone clicks the "start" button
def onClickStart():
    print("Start Button Pressed")

    global setpoint1
    global setpoint2
    global contactor1_SP
    global contactor2_SP

    # Set the current to zero amps
    setpoint1 = [0, 0, 0, 1, loadbank_test_config]
    setpoint2 = [0, 0, 0, 1, loadbank_test_config]
    # Close both contactors
    contactor1_SP = True
    contactor2_SP = True
    # If the combobox is set to a script fire that off
    global preprog_continue

    # invoke the special code for preprog mode
    if (run_param.get() == "preprog_selected"):
        preprog_continue = True
        run_preprog_mode()
        current_testing_status.set("Script Run")
    else:
        current_testing_status.set("Manual")


# Fires when someone clicks the "stop" button
def onClickStop():
    #print("Stop Button Pressed")
    current_testing_status.set("Stopped")

    global preprog_continue
    global routine_pointer

    # Reset the preprogrammed routine
    if (run_param.get() == "preprog_selected"):
        preprog_continue = False
        routine_pointer = 0

    global setpoint1
    global setpoint2
    global contactor1
    global contactor2

    # Set the current to zero amps
    setpoint1 = [0, 0, 0, 1, loadbank_test_config]
    setpoint2 = [0, 0, 0, 1, loadbank_test_config]
    # Open both contactors
    contactor1_SP = False
    contactor2_SP = False


# This checks the value of the user input box for Voltage Current or Power
def validate_float(var):
    #print("in the validate_float() function")
    old_value = ''
    new_value = var.get()
    try:
        new_value == '' or float(new_value)
        if (float(new_value) > 700 and run_param.get() == 'c_selected'):
            print('Current Draw Limits (700A) exceeded! Parameter too large!')
            var.set(old_value)
        elif (float(new_value) > 18000 and run_param.get() == 'pow_selected'):
            print('Power Draw Limits (18kW) exceeded! Parameter too large!')
            var.set(old_value)
    except:
        var.set(old_value)

        """
       else:
            if run_param.get() == 'c_selected':
                dc.set_TDI_state_ser1(float(new_value), 0, 0, 1, mode.get())
                dc.set_TDI_state_ser2(float(new_value), 0, 0, 1, mode.get())
            elif run_param.get() == 'v_selected':
                dc.set_TDI_state_ser1(0, float(new_value), 0, 2, mode.get())
                dc.set_TDI_state_ser2(0, float(new_value), 0, 2, mode.get())
            elif run_param.get() == 'pow_selected':
                dc.set_TDI_state_ser1(0, 0, float(new_value), 3, mode.get())
                dc.set_TDI_state_ser2(0, 0, float(new_value), 3, mode.get())
        """


def fetch():
    new_value = run_val.get()
    #print("Input => " + str(run_val.get()))  # get text

    global setpoint1
    global setpoint2
    global request_pending
    request_pending = True
    global mode


    if run_param.get() == 'c_selected':
        setpoint1 = [float(new_value), 0, 0, 1, loadbank_test_config] #dc.set_TDI_state_ser1(float(new_value), 0, 0, 1, mode.get())
        setpoint2 = [float(new_value), 0, 0, 1, loadbank_test_config] #dc.set_TDI_state_ser1(float(new_value), 0, 0, 1, mode.get())
    elif run_param.get() == 'v_selected':
        setpoint1 = [0, float(new_value), 0, 2, loadbank_test_config] #dc.set_TDI_state_ser1(0, float(new_value), 0, 2, mode.get())
        setpoint2 = [0, float(new_value), 0, 2, loadbank_test_config] #dc.set_TDI_state_ser2(0, float(new_value), 0, 2, mode.get())
    elif run_param.get() == 'pow_selected':
        setpoint1 = [0, 0, float(new_value), 3, loadbank_test_config] #dc.set_TDI_state_ser1(0, 0, float(new_value), 3, mode.get())
        setpoint2 = [0, 0, float(new_value), 3, loadbank_test_config] #dc.set_TDI_state_ser2(0, 0, float(new_value), 3, mode.get())

        


#Establish the first thread number
#thread = Thread(target=threaded_retriever_function)
thread_a = Thread(target=threaded_retriever_function_a)
thread_b = Thread(target=threaded_retriever_function_b)

root = Tk()
root.title("Battery Testing Application v1.0")
content = ttk.Frame(root, padding=(20, 20, 12, 12))

sv = StringVar()

# trace wants a callback with nearly useless parameters, fixing with lambda.
sv.trace('w', lambda nm, idx, mode, var=sv: validate_float(var))
# sv.trace('w', lambda nm, validate='enter', mode, var=sv: validate_float(var))

global mode
mode = StringVar()

global Contactor_LB1_Status_Old  # Allow hystersis on the diagnosing load bank 1 has faulted (stopping cooling flow)
Contactor_LB1_Status_Old = False

bank_mode_frame = Frame(content, bd=2, relief=SUNKEN, borderwidth=5)
run_mode_frame = Frame(content, bd=2, relief=SUNKEN, borderwidth=5)
preprog_mode_frame = Frame(content, bd=2, relief=SUNKEN, borderwidth=5)

a_option = ttk.Radiobutton(bank_mode_frame, text='Load Bank A (WCL 100-1000-12000)', variable=mode, value='a_only')
# b_option = ttk.Radiobutton(bank_mode_frame, text='Load Bank B (WCL 400-200-6000)', variable=mode, value='b_only')
both_option = ttk.Radiobutton(bank_mode_frame, text='Load Bank A&B (A & WCL 400-200-6000)', variable=mode, value='both')

global run_param
run_param = StringVar()

run_val = ttk.Entry(run_mode_frame, textvariable=sv)

run_val.bind('<Return>', (lambda event: fetch()))

volt_option = ttk.Radiobutton(run_mode_frame, text='Constant Voltage Setpoint', variable=run_param, value='v_selected')
current_option = ttk.Radiobutton(run_mode_frame, text='Constant Current Mode', variable=run_param, value='c_selected')
power_option = ttk.Radiobutton(run_mode_frame, text='Constant Power Mode', variable=run_param, value='pow_selected')
static_option = ttk.Radiobutton(preprog_mode_frame, text='Use Routine', variable=run_param, value='preprog_selected')

global predefinedmodevar
predefinedmodevar = StringVar()
predef = ttk.Combobox(preprog_mode_frame, textvariable=predefinedmodevar)
predef.bind('<<ComboboxSelected>>', print_selected())
predef['values'] = ('1: 440A / 320A', '2:Placeholder')#, '2: 320A/20Sec', '3: 440A/2Sec')

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

curr_mode_title = ttk.Label(content, text="Load Bank Selection", font=22)
curr_output_title = ttk.Label(content, text="CURRENT OUTPUT", font=22)
title_style = ttk.Style()
title_style.configure("GO.TButton", foreground="green", background="green")

heartbeat_frame = Frame(content, bd=2, relief=RAISED, borderwidth=5)

bank_output_frame = Frame(content, bd=2, relief=RAISED, borderwidth=5)

# Creating Text Labels for reach bank value,  Note for execution speed, feedback of values is commented out
#bank_1_current_output_text = ttk.Label(bank_output_frame, text="B1 Curr:")
#bank_1_volt_output_text = ttk.Label(bank_output_frame, text="B1 V: ")
bank_1_current_output_text = ttk.Label(bank_output_frame, text="")
bank_1_volt_output_text = ttk.Label(bank_output_frame, text="")
bank_1_load_output_text = ttk.Label(bank_output_frame, text="B1 Set Point: ")
bank_1_heartbeat_text = ttk.Label(heartbeat_frame, text="B1 Status:")
#bank_2_current_output_text = ttk.Label(bank_output_frame, text="B2 Curr:")
#bank_2_volt_output_text = ttk.Label(bank_output_frame, text="B2 V:")
bank_2_current_output_text = ttk.Label(bank_output_frame, text="")
bank_2_volt_output_text = ttk.Label(bank_output_frame, text="")
bank_2_load_output_text = ttk.Label(bank_output_frame, text="B2 Set Point:")
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

# ok = ttk.Button(content, text="Begin Testing", command=onClickStart, style="GO.TButton")
# cancel = ttk.Button(content, text="Stop", command=onClickStop, style="STOP.TButton")



buttons_frame = Frame(content, bd=2, borderwidth=5)

ok = ttk.Button(buttons_frame, text="Begin Testing", command=onClickStart, style="GO.TButton")
cancel = ttk.Button(buttons_frame, text="Stop", command=onClickStop, style="STOP.TButton")

###############
#
# Using Tkinter to populate out the UI in a grid layout
#
###############


testing_status.grid(column=5, row=0, sticky=W)
current_testing_status_screenvalue.grid(column=6, row=0, sticky=E)

curr_mode_title.grid(column=0, row=0, sticky=W)
a_option.grid(column=0, row=1, sticky=W)
# b_option.grid(column=0, row=2,sticky=W)
both_option.grid(column=0, row=3, sticky=W)
bank_mode_frame.grid(column=0, row=1, sticky=W + E + N + S)

# Populate Bank 1 output screen labels and vals
curr_output_title.grid(column=4, row=0, pady=5, padx=15, sticky=W + E)

bank_1_current_output_text.grid(column=0, row=0, padx=15, sticky=W)
bank_1_current_output_screenvalue.grid(column=1, row=0)

bank_1_volt_output_text.grid(column=0, row=1, padx=15, sticky=W)
bank_1_volt_output_screenvalue.grid(column=1, row=1)

bank_1_load_output_text.grid(column=0, row=2, padx=15, sticky=W)
bank_1_load_output_screenvalue.grid(column=1, row=2)

bank_2_current_output_text.grid(column=3, row=0, padx=15, sticky=W)
bank_2_current_output_screenvalue.grid(column=4, row=0)
bank_2_volt_output_text.grid(column=3, row=1, padx=15, sticky=W)
bank_2_volt_output_screenvalue.grid(column=4, row=1)
bank_2_load_output_text.grid(column=3, row=2, padx=15, sticky=W)
bank_2_load_output_screenvalue.grid(column=4, row=2)

bank_1_heartbeat_text.grid(column=0, row=0, sticky=W)
bank_1_heartbeat_screenvalue.grid(column=1, row=0, sticky=E)

bank_2_heartbeat_text.grid(column=0, row=1, sticky=W)
bank_2_heartbeat_screenvalue.grid(column=1, row=1, sticky=E)

heartbeat_frame.grid(column=5, row=1, columnspan=2, padx=5, pady=5, sticky=W + E + N + S)

bank_output_frame.grid(column=4, row=1, padx=5, pady=5, sticky=W + E + N + S)

run_val.grid(column=1, row=1, sticky=E)
input_header.grid(column=0, row=3, pady=15, sticky=W)
volt_option.grid(column=0, row=1, sticky=W)
current_option.grid(column=0, row=2, sticky=W)
power_option.grid(column=0, row=3, sticky=W)
static_option.grid(column=0, row=4, sticky=W)
predef.grid(column=1, row=4, columnspan=2)
run_mode_frame.grid(column=0, row=5, sticky=N + S + E + W)
preprog_mode_frame.grid(column=0, row=6)

# ok.grid(column=8, row=6, sticky=N+S+E+W)
# cancel.grid(column=8, row=7,  sticky=N+S+E+W)

ok.grid(column=0, row=0, columnspan=3, sticky=N + S + E + W)
cancel.grid(column=0, row=1, columnspan=3, sticky=N + S + E + W)
buttons_frame.grid(column=4, row=5, columnspan=3, sticky=N + S + E + W)

content.grid(column=0, row=0)

contact_info.grid(column=5, row=9, columnspan=3, sticky=E)

###############
#
# Think of this as the MAIN
#
###############

# Kick off the initial refresh sequence - lower to equal 500 to do it every .5 sec
root.after(2000, ui_refresh)

root.mainloop()
