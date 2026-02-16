# -*- coding: utf-8 -*-
##############################################################################
#
# Module: packetutils.py
#
# Description:
#     Packet encoding and decoding utilities for
#     Model 2450 communication protocol.
#
#     Provides helper APIs to read packetized
#     serial frames, decode protocol headers,
#     and extract payload data from packet
#     structures.
#
# Author:
#     Vinay N, MCCI Corporation Feb 16 2026
#
# Revision history:
#     v2.1.0  Wed Feb 16 2026 12:05:00  Vinay N
#         Module created
#
##############################################################################
import time

def decode_packet(packet_bytes):
    """
    Decode protocol packet structure.

    Extracts header fields and payload
    information from raw packet bytes.

    Packet Format:
        Byte 0:
            bit7 → Start bit
            bit6 → End bit
            bit5 → Reserved
            bit0–4 → Command

        Byte 1:
            bit5 - 7 → Sequence
            bit0 - 4 → Length

    Args:
        packet_bytes: Raw packet byte array.

    Returns:
        dict:
            Decoded packet fields including:
                start_bit
                end_bit
                reserved
                command
                sequence
                length
                payload

    Raises:
        ValueError:
            If packet length is invalid
            or header is incomplete.
    """
    
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
    """
    Read single packet frame from serial port.

    Reads header first to determine packet
    length, then fetches remaining payload.

    Args:
        ser: Active serial connection object.

    Returns:
        bytes | None:
            Complete packet frame if received,
            otherwise None.

    Raises:
        IOError:
            If serial read fails.
    """
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
    """
    Read block packet frame.

    Reads packet assuming full payload
    arrives in a single block transfer.

    Args:
        ser: Active serial connection object.

    Returns:
        bytes | None:
            Complete packet frame if valid,
            otherwise None.

    Raises:
        IOError:
            If serial read fails.
    """
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
