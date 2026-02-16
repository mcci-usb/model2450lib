# -*- coding: utf-8 -*-
##############################################################################
#
# Module: serialmodel.py
#
# Description:
#     Serial communication interface for MCCI Model 2450
#     BACK (Brightness And Color Kit).
#
#     Provides APIs to establish serial connection,
#     send protocol commands, receive packets, and
#     decode payload responses from the device.
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
import time
# Lib imports
import serial
import serial.tools.list_ports
# Own modules
from model2450lib.packetutils import decode_packet
from model2450lib.packetutils import read_packet_from_serial

class SerialDevice:
    """
    Serial device communication handler.

    This class manages serial connectivity,
    command transmission, packet decoding,
    and payload processing for Model 2450
    BACK devices.

    Attributes:
        port: Serial COM port.
        baudrate: Communication speed.
        ser: Serial connection object.
        keep_running: Streaming control flag.
    """
    def __init__(self, port):
        """
        Initialize SerialDevice instance.

        Args:
            port: Serial COM port name.

        Returns:
            None

        Raises:
            None
        """
        self.port = port
        self.baudrate = 115200
        self.ser = None
        self.keep_running = False

    def connect(self):
        """
        Establish serial connection.

        Opens serial port using configured
        communication parameters.

        Args:
            self: Instance reference.

        Returns:
            None

        Raises:
            serial.SerialException:
                If connection fails.
        """
        try:
            self.ser = serial.Serial(self.port, baudrate=self.baudrate, timeout=1)
        except Exception as e:
            print(f"Failed to connect: {e}")
            self.ser = None

    def disconnect(self):
        """
        Close serial connection.

        Safely terminates active
        device communication.

        Args:
            self: Instance reference.

        Returns:
            None

        Raises:
            None
        """
        if self.ser and self.ser.is_open:
            self.ser.close()
    def send_command(self, command):
        """
        Send raw command to device.

        Args:
            self: Instance reference.
            command: Command string.

        Returns:
            None

        Raises:
            IOError:
                If write operation fails.
        """
        if self.ser and self.ser.is_open:
            self.ser.write(command.encode())
            time.sleep(0.001)

    def read_and_process(self):
        """
        Read packets and process payload.

        Decodes incoming packets and
        reconstructs multi-frame payloads.

        Args:
            self: Instance reference.

        Returns:
            str | hex:
                ASCII payload string or
                hex string if non-ASCII.

        Raises:
            None
        """
        if not self.ser:
            return

        buffered_payload = b""

        while True:
            packet = read_packet_from_serial(self.ser)
            if packet:
                try:
                    # Decode the packet
                    decoded = decode_packet(packet)
                    payload = decoded.get("payload", b"")
                    start_bit = decoded["start_bit"]
                    end_bit = decoded["end_bit"]
                    reserved_bit = decoded["reserved"]
                    command = decoded["command"]
                    sequence = decoded["sequence"]
                    length = decoded["length"]

                    if start_bit:
                        buffered_payload = payload
                    else:
                        buffered_payload += payload

                    if end_bit or len(payload) < decoded["length"] - 2:
                        try:
                            ascii_payload = buffered_payload.decode("ascii").strip()
                            
                            # Optional filtering logic
                            if ascii_payload and ascii_payload[0].isalpha():
                                pass
                            elif ':' in ascii_payload:
                                pass

                            buffered_payload = b""  # Reset after processing

                            return ascii_payload  # ✅ Return here

                        except UnicodeDecodeError:
                            print("Non-ASCII Payload:", buffered_payload.hex())
                            buffered_payload = b""  # Also reset here in error case
                            return buffered_payload.hex()

                except Exception as decode_err:
                    print("Decode error:", decode_err)
            time.sleep(0.0006)
  
    def read_serial_data(self):
        """
        Stream and print serial payload data.

        Continuously reads decoded payloads
        and prints complete message lines.

        Args:
            self: Instance reference.

        Returns:
            None

        Raises:
            RuntimeError:
                If serial not connected.
        """
        if not self.ser:
            print("Serial not connected.")
            return

        buffer = b""

        while True:
            packet = read_packet_from_serial(self.ser)
            try:
                if packet:
                    decoded = decode_packet(packet)
                    payload = decoded["payload"]

                    buffer += payload

                    # Check if a complete message (ending with \r\n) is received
                    while b'\r\n' in buffer:
                        line, buffer = buffer.split(b'\r\n', 1)
                        # print(f"Actual payload: {line + b'\r\n'}")
                        full_line = line + b'\r\n'
                        print(f"Actual payload: {full_line}")
                        
                        # return full_line

            except Exception as e:
                print(f"Error reading data: {e}")

    def send_cmd(self, cmd):
        """
        Send command and get response.

        Utility wrapper combining
        send and receive operations.

        Args:
            self: Instance reference.
            cmd: Command string.

        Returns:
            str:
                Decoded payload response.

        Raises:
            None
        """
        self.send_command(cmd)
        return self.read_and_process()
    
    def send_stream_cmd(self, cmd):
        """
        Send command and stream response.

        Args:
            self: Instance reference.
            cmd: Command string.

        Returns:
            None

        Raises:
            None
        """

        self.send_command(cmd)
        return self.read_serial_data()
    
    def send_text_command(self, command, wait=2):
        """
        Send plain text command.

        Reads line-based textual responses
        from the device.

        Args:
            self: Instance reference.
            command: Text command string.
            wait: Response wait time (seconds).

        Returns:
            str:
                Aggregated response output.

        Raises:
            RuntimeError:
                If serial not connected.
        """
        if not self.ser or not self.ser.is_open:
            return "Serial port not connected.\n"

        self.ser.write(command.encode())
        output = f"[Sent TEXT command]: {command.strip()}\n"

        start_time = time.time()
        while time.time() - start_time < wait:
            if self.ser.in_waiting:
                try:
                    response = self.ser.readline().decode('utf-8', errors='ignore').strip()
                    if response:
                        output += f"{response}\n"
                except UnicodeDecodeError:
                    pass
            time.sleep(0.1)
        return output