##############################################################################
# 
# Module: searchswitch.py
#
# Description:
#     API to show list of available MCCI Model 2450 BACK (Brightness and Color Kit)
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
import time
import sys
import usb.util
from usb.backend import libusb1


def version():
    return "Model2450 v1.0.0"

def get_switches():
    devList = search_switches()
    return devList

def filter_port():
    usb_hwid_str = ["USB VID:PID=045E:0646"]
    comlist = serial.tools.list_ports.comports()
    port_name = []

    for port, desc, hwid in sorted(comlist):
        res = [True for gnhwid in usb_hwid_str if(gnhwid in hwid)]
        if(res):
            port_name.append(port)
    return port_name

def search_switches():
    port_name = []
    rev_list = []
    dev_list = []

    port_name = filter_port()

    for i in range(len(port_name)):
        try:
            ser = serial.Serial(port=port_name[i], baudrate=115200, 
                                bytesize=serial.EIGHTBITS,
                                parity=serial.PARITY_NONE, timeout=1, 
                                stopbits=serial.STOPBITS_ONE)
           
            time.sleep(1)
    
            cmd = 'version\r\n'
            print("cmd:", cmd)
            ser.write(cmd.encode())
            strout = ser.readline().decode('utf-8')
            nstr = strout[2:]
            print("nstr:",nstr)
            if(nstr.find('1') != -1):
                rev_list.append(port_name[i])
                dev_list.append('2450')
            
            ser.close()
        except serial.SerialException as e:
            pass

    rdict = {}
    devlist = []
    
    for i in range(len(rev_list)):
        tempdict = {}
        tempdict["port"] = rev_list[i]
        tempdict["model"] = dev_list[i]
        devlist.append(tempdict)

    rdict["switches"] = devlist
    return rdict