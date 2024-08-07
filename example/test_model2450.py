# avalaible list of MCCI Switches with port number
# from model2450 import searchswitch

# import searchswitch
# import switch2450

import time
from model2450lib import searchswitch
from model2450lib import switch2450
# found a list of available switches.
# using the port number open the switch.
dev_list = searchswitch.get_switches()
# print(dev_list)

sw1 = switch2450.Switch2450('COM3')
# print("switch 2450 connected:", sw1)
# Connect the USB Switch
sw1.connect()
print("Connected switch 2450:")


# sw1.get_version()

# # sw1.get_version_rd()

# sw1.read_sn()

# sw1.level_read()

# sw1.get_read()

# sw1.color_read()
# # sw1.color_read()

# print("First call to color_read:")
# result = sw1.color_read()

for _ in range(30):
    sw1.color_read()

    sw1.level_read()
    
    sw1.get_read()
    






# sw1.color_read()

# sw1.level_read()

# sw1.get_read()

# sw1.color_read()

# sw1.read_level_RGB()

# # sw1.get_read()

# # sw1.read_level()

# # sw1.get_color()
# sw1.get_color()
# # # print
# response = sw1.get_color()
