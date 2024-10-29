##############################################################################
# 
# Module: model2450.py
#
# Description:
#     Top level API to manage Model 2450
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
from model2450lib import model

class Model2450(model.Model):
    def __init__(self, cport):
        model.Model.__init__(self, cport, 115200)
    
    def read_sn(self):
        cmd = 'sn\r\n'
        rc, rstr = self.send_cmd(cmd)
        # print(rc,rstr)
        return (rstr)
    
    def get_version(self):
        cmd = 'version\r\n'
        rc, rstr =  self.send_cmd(cmd)
        # print("rstr-version:", rstr)
        return (rc, rstr)
    
    def do_reset(self):
        cmd = 'reset\r\n'
        rc, rstr =  self.send_cmd(cmd)
        # print("rstr-version:", rstr)
        return (rc, rstr)

    
    def get_read(self):
        cmd = 'read\r\n'
        rc, rstr = self.send_cmd(cmd)
        # print("read->:",rstr)
        return (rstr)

    
    def get_level(self):
        cmd = 'level\r\n'
        rc, rstr = self.send_cmd(cmd)
        # print("level->", rstr)
        return rstr
    
    def set_level(self, value):
        cmd = self.set_level_cmd(value)
        return self.send_cmd(cmd)
    
    def set_level_cmd(self, value):
        return 'level '+str(value)+'\r\n'
    
  
    def get_color(self):
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
    
    # def set_th_light(self):
    #     cmd = "level"

    def set_run(self):
        cmd = 'run\r\n'
        rc, rstr = self.send_blinkcommand(cmd)
        # print(f"run command output:\n{rstr}")
        return rstr
 
    def set_stop(self):
        cmd = 'stop\r\n'
        rc, rstr = self.send_blinkcommand(cmd)
        # print(f"stop command output:\n{rstr}")
        return rstr
