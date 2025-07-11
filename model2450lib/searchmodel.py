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
#     Vinay N, MCCI Corporation May 2025
#
# Revision history:
#    V1.0.1 Wed May 2025 12:05:00   Vinay N
#       Module created
##############################################################################
import serial
import serial.tools.list_ports
import time
import sys
import usb.util
from usb.backend import libusb1
# from packetutils import read_packet_from_serial, decode_packet
from .packetutils import read_packet_from_serial, decode_packet


def version():
    return "Model2450 v1.0.0"

def get_models():
    devList = search_models()
    return devList

def get_avail_ports():
    comlist = serial.tools.list_ports.comports()
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

        # Send version command and try to decode the response
        ser.write(b'version\r\n')
        time.sleep(0.1)
        raw_packet = read_packet_from_serial(ser)

        if raw_packet:
            try:
                decoded = decode_packet(raw_packet)
                payload_str = bytes(decoded["payload"]).decode('ascii', errors='ignore')
                if '3:1' in payload_str or '8:1' in payload_str or '9:1' in payload_str:
                    ser.close()
                    return '2450'
            except Exception as e:
                print(f"Packet decoding failed: {e}")

        # If version didn't return valid result, try status
        ser.write(b'status\r\n')
        time.sleep(0.1)
        raw_packet = read_packet_from_serial(ser)

        if raw_packet:
            try:
                decoded = decode_packet(raw_packet)
                payload_str = bytes(decoded["payload"]).decode('ascii', errors='ignore')
                if 'Brightness And Color Kit' in payload_str:
                    ser.close()
                    return '2450'
            except Exception as e:
                print(f"Packet decoding failed: {e}")

        ser.close()
        return None

    except serial.SerialException as e:
        print(f"Serial communication error: {e}")
        return None

    except Exception as e:
        print(f"Unexpected error: {e}")
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