from tkinter import *
from tkinter import ttk


def print_selected(): {
    print("Combobox changed")
}

root = Tk()
root.title("Battery Testing Application v0.1")
content = ttk.Frame(root)

mode = StringVar()
simul_option = ttk.Radiobutton(content, text='Test Banks Simul', variable=mode, value='simul')
individ_option = ttk.Radiobutton(content, text='Test Banks Indiv', variable=mode, value='individual')

run_param = StringVar()
run_val = ttk.Entry(content)
volt_option = ttk.Radiobutton(content, text='V Input', variable=run_param, value='v_selected')
current_option = ttk.Radiobutton(content, text='C Input', variable=run_param, value='c_selected')
power_option = ttk.Radiobutton(content, text='Pow Input', variable=run_param, value='pow_selected')
static_option = ttk.Radiobutton(content, text='Use PreProg', variable=run_param, value='preprog_selected')


predefinedmodevar = StringVar()
predef = ttk.Combobox(content, textvariable=predefinedmodevar)
predef.bind('<<ComboboxSelected>>', print_selected())
predef['values'] = ('Pre-defined 1', 'Pre-defined 2', 'Pre-defined 3')

namelbl = ttk.Label(content, text="Name")
name = ttk.Entry(content)

contact_info = ttk.Label(content, text="Built by Dan Harris - dan.harris@gmail.com")

testing_status = ttk.Label(content, text="TESTING STATUS: INACTIVE ")

bank_1_current_output_label = ttk.Label(content, text="B1 Curr: 5")
bank_1_volt_output_label = ttk.Label(content, text="B1 V: 13")
bank_1_load_output_label = ttk.Label(content, text="B1 Load: 10")
bank_1_heartbeat = ttk.Label(content, text="B1 Status: Online")

bank_2_current_output_label = ttk.Label(content, text="B2 Curr: 12")
bank_2_volt_output_label = ttk.Label(content, text="B2 V: 50")
bank_2_load_output_label = ttk.Label(content, text="B2 Load: 100")
bank_2_heartbeat = ttk.Label(content, text="B2 Status: Online")

onevar = BooleanVar()
twovar = BooleanVar()
threevar = BooleanVar()
onevar.set(True)
twovar.set(False)
threevar.set(True)

ok = ttk.Button(content, text="Begin Testing")
cancel = ttk.Button(content, text="Stop")


testing_status.grid(column=7, row=0)
simul_option.grid(column=0, row=1)
individ_option.grid(column=0, row=2)

bank_1_current_output_label.grid(column=2, row=1)
bank_1_volt_output_label.grid(column=2, row=2)
bank_1_load_output_label.grid(column=2, row=3)
bank_1_heartbeat.grid(column=7, row=1)

bank_2_current_output_label.grid(column=4, row=1)
bank_2_volt_output_label.grid(column=4, row=2)
bank_2_load_output_label.grid(column=4, row=3)
bank_2_heartbeat.grid(column=7, row=2)


run_val.grid(column=6, row=4)
volt_option.grid(column=4, row=4)
current_option.grid(column=4, row=5)
power_option.grid(column=4, row=6)
static_option.grid(column=4, row=7)

ok.grid(column=7, row=5)
cancel.grid(column=7, row=6)

content.grid(column=0, row=0)
predef.grid(column=5, row=7, columnspan=2)
contact_info.grid(column=6, row=8, columnspan=3)

root.mainloop()