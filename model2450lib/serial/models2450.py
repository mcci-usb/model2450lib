##############################################################################
# 
# Module: models2450.py
#
# Description:
#     Top level API to manage Model 2450
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

from model2450lib.serial import models 

class Models2450(models.Switch):
    def __init__(self, cport):
        models.Switch.__init__(self, cport, 115200)
    
    def get_status(self):
        cmd = 'status\r\n'
        rc, rstr = self.send_status_cmd(cmd) 
        return(rc, rstr)

    def get_orientation(self):
        strin = "--"
        rc, rstr = self.get_status()
        if rc == 0:
            outstr = rstr.split('\n')
            cc1detect = None
            cc1led = None
            for instr in outstr:
                if 'CC1 detect:' in instr:
                    fstr = instr.split('0x')
                    cc1detect = int(fstr[1], 16)
                elif 'CC1 led:' in instr:
                    lstr = instr.split(':')
                    cc1led = int(lstr[1])
                    break
            if cc1led == 0 and cc1detect < 20:
                    strin = "Flip"
            elif cc1led == 1 and cc1detect > 20:
                strin = "Normal"
            return (rc, strin)
        else:
            return (rc, "ComError")
    
    def do_reset(self):
        cmd = 'reset -b\r\n'
        rc, rstr = self.send_reset(cmd) 
        return(rc, rstr)
    
    def get_volts(self):
        cmd = 'volts\r\n'
        rc, rstr = self.send_cmd(cmd)
        return (rc, rstr)

    def get_amps(self):
        cmd = 'amps\r\n'
        rc, rstr = self.send_cmd(cmd)
        return (rc, rstr)