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

# Replace 'COMX' with the appropriate COM port for Model2450 
sw1 = model2450.Model2450('COM6')
# print("switch 2450 connected:", sw1)
# Connect the USB Switch
sw1.connect()
print("Connected switch 2450:")

sn= sw1.read_sn()  # cmd for read serial number
print(sn)

time.sleep(1)
gread = sw1.get_read() # cmd for read the ambient light sensor
print(gread)

time.sleep(1)
gread = sw1.get_read() # cmd for read the ambient light sensor
print(gread)

time.sleep(1)
gread = sw1.get_read() # cmd for read the ambient light sensor
print(gread)

time.sleep(1)
gcolor = sw1.get_color() # display the color reading
print(gcolor)

time.sleep(1)
gcolor = sw1.get_color() # display the color reading
print(gcolor)

time.sleep(1)
gcolor = sw1.get_color() # display the color reading
print(gcolor)

time.sleep(1)
glevel = sw1.get_level() # cmd for read the light level for detecting blank frames
print(glevel)

time.sleep(1)
gcolor = sw1.get_color() # display the color reading
print(gcolor)

