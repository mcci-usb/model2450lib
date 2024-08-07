##############################################################################
# 
# Module: switch.py
#
# Description:
#     API to send commands 
#
#     Released under the MCCI Corporation.
#
# Author:
#     Vinay N, MCCI Corporation August 2024
#
# Revision history:
#    V1.0.0 Wed Aug 2024 12:05:00   Vinay N
#       Module created
##############################################################################

from model2450lib import serialswitch

class Switch(serialswitch.SerialDev):
    def __init__(self, cport, baud):
        self.sport = serialswitch.SerialDev(cport, baud)
    
    def connect(self):
        return self.sport.open()

    def disconnect(self):
        return self.sport.close()

    def get_version(self):
        cmd = 'version\r\n'
        return self.send_cmd(cmd)
    
    def send_cmd(self, cmd):
        # self.clear_buffer()  # Clear buffer before sending command
        # print(cmd)
        res = self.sport.write(cmd)
        if res > 0:
            res, rstr = self.sport.read()
        else:
            rstr = "Comm Error\n"
        return res, rstr
    
    def send_command(self, cmd):
        # self.write(cmd.encode('utf-8') + b'\r\n')
        # self.sport.write(cmd.encode('utf-8') + b'\r\n')
        re = self.sport.write(cmd)
        response1 = self.sport.readcolor()
        response2 = self.sport.readcolor()

        return re, response1
