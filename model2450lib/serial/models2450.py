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

    def do_reset(self):
        cmd = 'reset -b\r\n'
        rc, rstr = self.send_reset(cmd) 
        return(rc, rstr)
    