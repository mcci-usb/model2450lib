##############################################################################
# 
# Module: models.py
#
# Description:
#     API to send commands 
#
#     Released under the MCCI Corporation.
#
# Author:
#     Vinay N, MCCI Corporation May 2025
#
# Revision history:
#    V1.0.1 Wed May 2025 12:05:00   Vinay N
#       Module created
##############################################################################

from model2450lib.serial import serialmodels

class Switch(serialmodels.SerialDev):
    def __init__(self, cport, baud):
        self.sport = serialmodels.SerialDev(cport, baud)
    
    def connect(self):
        return self.sport.open()

    def disconnect(self):
        return self.sport.close()

    def get_version(self):
        cmd = 'version\r\n'
        return self.send_cmd(cmd)

    def send_cmd(self, cmd):
        res = self.sport.write(cmd)
        if res > 0:
            res, rstr = self.sport.read()
        else:
            rstr = "Comm Error\n"
        return res, rstr
    
    def send_reset(self, cmd):
        res = self.sport.write(cmd)
        if res > 0:
            rstr = "success\n"
        else:
            rstr = "Comm Error\n"
        return res, rstr

    def send_status_cmd(self, cmd):
        outstr = ""
        res = self.sport.write(cmd)
        if res > 0:
            for i in range(25):
                res, rstr = self.sport.read()
                if res == 0:
                    outstr = outstr + rstr
        elif res == 0:
            outstr = "Comm Error\n"
        return res, outstr