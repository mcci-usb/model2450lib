##############################################################################
# 
# Module: searchmodel.py
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

def get_models():
    devList = search_models()
    return devList

def get_avail_ports():
    comlist = serial.tools.list_ports.comports()
    print("comlist:", comlist)
    port_name = []
    for port, desc, hwid in sorted(comlist):
        port_name.append((hwid, port, desc))
    return port_name

def filter_port():
    usb_hwid_str = ["USB VID:PID=045E:0646"]
    comlist = serial.tools.list_ports.comports()
    port_name = []

    for port, desc, hwid in sorted(comlist):
        res = [True for gnhwid in usb_hwid_str if(gnhwid in hwid)]
        if(res):
            port_name.append(port)
    return port_name

def check_status(myport):
    try:
        ser = serial.Serial(myport, baudrate=115200, 
                            bytesize=serial.EIGHTBITS,
                            parity=serial.PARITY_NONE, timeout=1, 
                            stopbits=serial.STOPBITS_ONE)
        time.sleep(1)

        status_cmd = 'status\r\n'

        ser.write(status_cmd.encode())
        strout = ser.readline().decode('utf-8')
        
        # Waiting for the complete response
        start_time = time.time()
        while (time.time() - start_time) < 2:
            line = ser.readline().decode('utf-8')
            strout += line

        ser.close()
        
        if 'Brightness And Color Kit' in strout:
            return '2450'
        else:
            return None

    except serial.SerialException as e:
        return None

def search_models():
    port_name = filter_port()
    rev_list = []
    dev_list = []

    for i in range(len(port_name)):
        model = check_status(port_name[i])
        if model is not None:
            rev_list.append(port_name[i])
            dev_list.append(model)

    rdict = {}
    devlist = []
    
    for i in range(len(rev_list)):
        tempdict = {}
        tempdict["port"] = rev_list[i]
        tempdict["model"] = dev_list[i]
        devlist.append(tempdict)

    rdict["models"] = devlist
    return rdict
