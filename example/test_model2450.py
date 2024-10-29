# avalaible list of MCCI Switches with port number
# from model2450 import searchswitch

# import searchswitch
# import switch2450

import time
from model2450lib import searchmodel
from model2450lib import model2450
# found a list of available switches.
# using the port number open the switch.
dev_list = searchmodel.get_models()
print(dev_list)

sw1 = model2450.Model2450('COM4')
# print("switch 2450 connected:", sw1)
# Connect the USB Switch
sw1.connect()
print("Connected switch 2450:")


time.sleep(1)
sRun = sw1.set_run()
print("run blank frames....:")

time.sleep(10)
rStop = sw1.set_stop()
print("stop blank frames....:")

# time.sleep(1)
# ser = sw1.read_sn()  # READ SERIAL NUMBER
# print(ser)
# time.sleep(1)
# ver = sw1.get_version()  # VERSION F:H
# print(ver)
# time.sleep(1)
# gRead = sw1.get_read()  # READ
# print(gRead)
# time.sleep(1)
# cRead = sw1.get_color()   # COLOR Values
# print(cRead)
# time.sleep(1)
# lRead = sw1.get_level()   # LEVEL
# print(lRead)
