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

    def port_on(self, pno):
        cmd = self.port_cmd(pno)
        return self.send_cmd(cmd)

    def port_off(self):
        cmd = self.port_cmd(0)
        return self.send_cmd(cmd)

    def get_port_status(self):
        cmd = 'port\r\n'
        return self.send_cmd(cmd)

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

    def port_cmd(self, pno):
        return 'port '+str(pno)+'\r\n'

    def set_speed(self, speed):
        if speed == "SS":
            val = 1
        else:
            val = 0
        cmd = 'superspeed'+' '+str(val)+'\r\n'
        res, outstr = self.send_cmd(cmd)
        if res == 0:
            outstr = outstr.replace('s', 'S')
            outstr = outstr.replace('1', 'Enabled')
            outstr = outstr.replace('0', 'Disabled')
        return res, outstr

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