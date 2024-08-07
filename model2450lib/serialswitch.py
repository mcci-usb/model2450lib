##############################################################################
# 
# Module: serialswitch.py
#
# Description:
#     serialswitch is shows serial port devices
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
import serial
import serial.tools.list_ports

class SerialDev:
    def __init__(self, port, baud):
        print("Serial Constructor")
        self.handler = None
        self.port = port
        self.baud = baud

    def open(self):
        self.handler = serial.Serial()
        self.handler.port = self.port
        self.handler.baudrate = self.baud
        self.handler.bytesize = serial.EIGHTBITS
        self.handler.parity = serial.PARITY_NONE
        self.handler.timeout = 1
        self.handler.stopbits =serial. STOPBITS_ONE
        
        try:
            res = self.handler.open()
            return True
        except serial.SerialException as e:
            return False
            
    def close(self):
        try:
            self.handler.close()
            return True
        except:
            return False

    def write(self, cmd):
        try:
            cnt = self.handler.write(cmd.encode())
            return cnt
        except:
            return -1

    def read(self):
        try:
            return  0, self.handler.readline().decode('utf-8')
        except:
            return -1
    

    def readcolor(self):
        try:
            self.res1 = self.handler.readline().decode('utf-8').strip()
            self.res2 = self.handler.readline().decode('utf-8').strip()

            # return self.res2 Actual return

            return self.res2

        except:
            return " "
    
    