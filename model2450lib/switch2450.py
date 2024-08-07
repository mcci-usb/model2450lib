##############################################################################
# 
# Module: switch2450.py
#
# Description:
#     Top level API to manage USB Switch 2450
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
from model2450lib import switch


class Switch2450(switch.Switch):
    def __init__(self, cport):
        switch.Switch.__init__(self, cport, 115200)
    
    def read_sn(self):
        cmd = 'sn\r\n'
        rc, rstr = self.send_cmd(cmd)
        # print(rc,rstr)
        return (rstr)
    
    def get_version_rd(self):
        cmd = 'version\r\n'
        rc, rstr =  self.send_cmd(cmd)
        # print("rstr-version:", rstr)
        return (rc, rstr)
    

    
    def get_read(self):
        cmd = 'read\r\n'
        rc, rstr = self.send_cmd(cmd)
        # print("read->:",rstr)
        return (rstr)

    
    def level_read(self):
        cmd = 'level\r\n'
        rc, rstr = self.send_cmd(cmd)
        # print("level->", rstr)
        return rstr
    
    # def send_cmd(self, cmd):
    #     self.ser.write(cmd.encode())
    #     response = self.ser.read_until(b'\r\n\r\n').decode()  # Read until double CRLF
    #     return 0, response send_command

    def color_read(self):
        cmd = 'color\r\n'
        rc, rstr = self.send_command(cmd)
        # print("color->", rstr)
        return rstr


    def set_red(self):
        cmd = 'set red\r\n'
        rc, rstr = self.send_cmd(cmd)
        return rstr
    
    def set_blue(self):
        cmd = 'set blue\r\n'
        rc, rstr = self.send_cmd(cmd)
        return rstr

    def set_green(self):
        cmd = 'set green\r\n'
        rc, rstr = self.send_cmd(cmd)
        return rstr
    
    
   
    


  


