# packetutils.py
##############################################################################
# 
# Module: packetutils.py
#
# Description:
#     this is decoding and encoding the commands when command is enable
#     under packetaization format.
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
import time

def decode_packet(packet_bytes):
    # print("packet_bytes:", packet_bytes)
    
    if len(packet_bytes) < 2:
        raise ValueError("Packet too short to decode header.")

    header_byte_0 = packet_bytes[0]
    header_byte_1 = packet_bytes[1]

    start_bit = (header_byte_0 >> 7) & 0x01
    end_bit = (header_byte_0 >> 6) & 0x01
    reserved = (header_byte_0 >> 5) & 0x01
    command = header_byte_0 & 0x1F

    sequence = (header_byte_1 >> 5) & 0x07
    length = header_byte_1 & 0x1F

    if len(packet_bytes) < length:
        raise ValueError(f"Packet length mismatch. Expected {length}, got {len(packet_bytes)}")

    payload = packet_bytes[2:length]

    return {
        "start_bit": start_bit,
        "end_bit": end_bit,
        "reserved": reserved,
        "command": command,
        "sequence": sequence,
        "length": length,
        "payload": payload
    }

def read_packet_from_serial(ser):
    header = ser.read(2)
    if len(header) < 2:
        return None

    length = header[1] & 0x1F
    remaining = length - 2

    # Read the remaining payload robustly
    payload = b""
    while len(payload) < remaining:
        more = ser.read(remaining - len(payload))
        if not more:
            return None
        payload += more

    return header + payload

def read_block_frames(ser):
    header = ser.read(2)
    # print("......header:", header)
    if len(header) < 2:
        return None

    length = header[1] & 0x1F
    remaining = length - 2
    payload = ser.read(remaining)
    if len(payload) < remaining:
        return None

    return header + payload
