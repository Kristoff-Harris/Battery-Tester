# This is used by Chris for UI testing as that's the only way I can get the UI to populate as if it had real data
# If this is too basic or the data isn't legit, we can update it
def getBank1ConnStatus():
    return True


def getBank2ConnStatus():
    return True


def getBank1Voltage():
    return 3


def getBank2Voltage():
    return 4


def getBank1Current():
    return 6


def getBank2Current():
    return 11


def getBank1Load():

    return 24


def getBank2Load():

    return 6

#what should this return?
def queryTDI_ser1(write_str):
    return "something"


def queryTDI_ser2(write_str):
    return "something"


def set_TDI_state_ser1(curr, volt, power, mode):

    return


def set_TDI_state_ser2(curr, volt, power, mode):
    return


def open_TDI1_contactor():
    return True


def open_TDI2_contactor():
    return True


def close_TDI1_contactor():
    return True


def close_TDI2_contactor():
    return True
