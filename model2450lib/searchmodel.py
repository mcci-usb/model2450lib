# -*- coding: utf-8 -*-
##############################################################################
#
# Module: searchmodel.py
#
# Description:
#     API to scan and list available MCCI Model 2450
#     BACK (Brightness and Color Kit) devices.
#
#     Provides utilities to detect connected devices,
#     filter supported USB ports, and validate device
#     identity using protocol commands.
#
# Author:
#     Vinay N, MCCI Corporation Feb 16 2026
#
# Revision history:
#     v2.1.0  Wed Feb 16 2026 12:05:00  Vinay N
#         Module created
#
##############################################################################
# Built-in imports
import sys
import time

# Lib imports
import serial
import serial.tools.list_ports
import usb.util
from usb.backend import libusb1

# Own modules
from .packetutils import read_packet_from_serial
from .packetutils import decode_packet

def version():
    """
    Get library version information.

    Args:
        None

    Returns:
        str:
            Library version string.

    Raises:
        None
    """
    return "Model2450 2.1.0"

def get_models():
    """
    Retrieve list of detected Model 2450 devices.

    Args:
        None

    Returns:
        dict:
            Dictionary containing detected model
            device details.

    Raises:
        None
    """
    devList = search_models()
    return devList

def get_avail_ports():
    """
    Get all available COM ports.

    Scans system serial interfaces and
    returns port hardware details.

    Args:
        None

    Returns:
        list:
            List of tuples containing
            (HWID, Port, Description).

    Raises:
        None
    """
    comlist = serial.tools.list_ports.comports()
    port_name = []
    for port, desc, hwid in sorted(comlist):
        port_name.append((hwid, port, desc))
    return port_name

def filter_port():
    """
    Filter supported USB ports.

    Identifies ports matching Model 2450
    USB VID/PID pattern.

    Args:
        None

    Returns:
        list:
            Filtered COM port list.

    Raises:
        None
    """
    usb_hwid_str = ["USB VID:PID=045E:0646"]
    comlist = serial.tools.list_ports.comports()
    port_name = []

    for port, desc, hwid in sorted(comlist):
        res = [True for gnhwid in usb_hwid_str if(gnhwid in hwid)]
        if(res):
            port_name.append(port)
    return port_name

def check_status(myport):
    """
    Validate device identity on a port.

    Sends protocol commands to confirm whether
    connected device is Model 2450 BACK kit.

    Args:
        myport: Serial COM port name.

    Returns:
        str | None:
            Returns model number if detected,
            otherwise None.

    Raises:
        serial.SerialException:
            If serial communication fails.
    """
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
    """
    Scan system for available Model 2450 devices.

    Filters supported ports and validates each
    device using protocol status checks.

    Args:
        None

    Returns:
        dict:
            Dictionary containing detected
            model and port mapping.

            Example:
            {
                "models": [
                    {"port": "COM3", "model": "2450"}
                ]
            }
    Raises:
        None
    """
    
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