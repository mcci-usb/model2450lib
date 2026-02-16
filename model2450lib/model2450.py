# -*- coding: utf-8 -*-
##############################################################################
#
# Module: model2450.py
#
# Description:
#     Top-level API to manage Model 2450
#     BACK (Brightness And Color Kit).
#
#     Provides high-level command wrappers
#     for device control, configuration,
#     streaming, and operational modes.
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

# Own modules
from model2450lib.serialmodel import SerialDevice
from model2450lib.packetutils import decode_packet
from model2450lib.packetutils import read_packet_from_serial
from model2450lib.packetutils import read_block_frames

class Model2450(SerialDevice):
    """
    Model 2450 BACK — Brightness And Color Kit

    Hardware Components:
        • OPT4001 Ambient Light Sensor
        • BH1749 Color Sensor

    This device supports ambient light measurement,
    RGB color sensing, blank frame detection,
    calibration storage, streaming telemetry,
    and EEPROM tag operations.
    """
    def __init__(self, port):
        """
        Initialize Model2450 interface.

        Args:
            port: Serial COM port name.

        Returns:
            None

        Raises:
            None
        """
        super().__init__(port)
        self.r_data = []
        self.g_data = []
        self.b_data = []
        self.light_data = []
        self.time_data = []
        self.keep_running = True

    def read_sn(self):
        """
        Read device serial number.

        Sends SN command to retrieve the
        unique serial number stored in EEPROM.

        Args:
            None

        Returns:
            str:
                Serial number string.

        Raises:
            RuntimeError:
                If device communication fails.
        """
        return self.send_cmd('sn\r\n')

    def get_version(self):
        """
        Get firmware and hardware version.

        Version format:
            F:H
            F → Firmware version
            H → Hardware version

        Args:
            None

        Returns:
            str:
                Version information string.

        Raises:
            RuntimeError:
                If command execution fails.
        """
        return self.send_cmd('version\r\n')

    def get_color(self):
        """
        Read RGB color sensor values.

        Retrieves color readings from
        BH1749 color sensor.

        Args:
            None

        Returns:
            str:
                RGB measurement data.

        Raises:
            RuntimeError:
                If sensor read fails.
        """
        return self.send_cmd('color\r\n')

    def get_read(self):
        """
        Read ambient light sensor value.

        Retrieves lux data from the
        OPT4001 ambient light sensor.

        Args:
            None

        Returns:
            str:
                Ambient light measurement.

        Raises:
            RuntimeError:
                If sensor read fails.
        """
        return self.send_cmd('read\r\n')

    def get_level(self):
        """
        Get blank frame detection level.

        Reads configured light threshold
        used for black frame detection.

        Args:
            None

        Returns:
            str:
                Current detection level.

        Raises:
            RuntimeError:
                If read fails.
        """
        return self.send_cmd('level\r\n')
    
    def set_red(self):
        """
        Calibrate red channel.

        Stores calibration reference
        for red color.

        Note:
            Place sensor over red display
            region before executing.

        Returns:
            str:
                Calibration response.
        """
        return self.send_cmd('set red\r\n')
    
    def set_blue(self):
        """
        Calibrate blue channel.

        Stores calibration reference
        for blue color.

        Note:
            Place sensor over blue display
            region before executing.

        Returns:
            str:
                Calibration response.
        """
        return self.send_cmd('set blue\r\n')
    
    def set_green(self):
        """
        Calibrate green channel.

        Stores calibration reference
        for green color.

        Note:
            Place sensor over green display
            region before executing.

        Returns:
            str:
                Calibration response.
        """
        return self.send_cmd('set green\r\n')
    
    def set_run(self):
        """
        Start blank frame detection.

        Device begins scanning
        for black frames.

        Returns:
            str:
                Run mode response.
        """
        return self.send_text_command('run\r\n')
    
    def set_stop(self):
        """
        Stop blank frame detection.

        Stops scanning and prints
        detection results.

        Returns:
            str:
                Stop response output.
        """
        return self.send_text_command('stop\r\n')

    def do_reset(self):
        """
        Perform bootloader reset.

        Resets device into firmware
        update mode.

        Returns:
            None
        """
        try:
            self.send_command('reset -b\r\n')
            time.sleep(0.1)  # Give time for device to reset
            self.disconnect()  # Close serial port cleanly
        except Exception as e:
            print(f"Ignoring expected error during reset: {e}")
            
    def reset_mode(self):
        """
        Perform device reset.

        Reboots device for firmware
        or configuration updates.

        Returns:
            None
        """
        try:
            self.send_command('reset\r\n')
            time.sleep(0.1)  # Give time for device to reset
            self.disconnect()  # Close serial port cleanly
        except Exception as e:
            print(f"Ignoring expected error during reset: {e}")

    def set_level(self, value):
        """
        Set blank frame detection level.

        Configures light threshold used
        to detect blank frames.

        Args:
            value:
                Detection level value.

        Returns:
            str:
                Device acknowledgement.

        Raises:
            ValueError:
                If value is invalid.
        """
        cmd = f'level {value}\r\n'
        return self.send_cmd(cmd)
    
    def get_stream3(self, callback=None):
        """
        Start dual sensor streaming.

        Streams ambient light and
        color sensor data.

        Args:
            callback:
                Optional handler function
                to process streamed data.

        Returns:
            None
        """
        self.send_stream_cmd("stream 3\r\n")  # or whatever command starts the stream

        while self.ser and self.ser.is_open:
            packet = read_packet_from_serial(self.ser)
            if packet:
                try:
                    decoded = decode_packet(packet)
                    payload = decoded.get("payload", b"")
                    ascii_payload = payload.decode("ascii", errors="ignore").strip()
                    
                    if ascii_payload:
                        print(f"[get_stream3] Received: {ascii_payload}")
                        if callback:
                            callback(ascii_payload)

                except Exception as e:
                    print(f"[get_stream3] Decode error: {e}")

  
    def run_blank_frame_sequence(self, duration=10):
        """
        Execute blank frame detection sequence.

        Runs detection for specified duration
        and counts blank frames.

        Args:
            duration:
                Detection runtime (seconds).

        Returns:
            int:
                Blank frame count.
        """
        self.ser.write(b"run\r\n")  # Use self.ser instead of ser

        start_time = time.time()  # Track the start time
        buffered_payload = b""
        blank_frame_count = 0  # Initialize a counter for blank frames

        while self.ser and self.ser.is_open:
            # Check if the elapsed time has passed the duration
            if time.time() - start_time >= duration:
                self.stop_blank_frame_sequence()  # Stop the sequence after the specified duration
                break

            packet = read_block_frames(self.ser)
            if packet:
                try:
                    decoded = decode_packet(packet)
                    payload = decoded.get("payload", b"")
                    start_bit = decoded["start_bit"]
                    end_bit = decoded["end_bit"]
                    if start_bit:
                        buffered_payload = payload
                    else:
                        buffered_payload += payload

                    if end_bit or len(payload) < decoded["length"] - 2:
                        try:
                            ascii_payload = buffered_payload.decode("ascii").strip()
                            if not ascii_payload:  # Consider empty payload as blank frame
                                blank_frame_count += 1
                        except UnicodeDecodeError:
                            print(f"payload: {buffered_payload.hex()} (non-ascii)")
                        buffered_payload = b""

                except Exception as decode_err:
                    print("Decode error:", decode_err)

            time.sleep(0.0006)

        return blank_frame_count  # Return the count of blank frames detected

    def stop_blank_frame_sequence(self):
        """
        Stop blank frame sequence.

        Returns:
            None
        """
        self.ser.write(b"stop\r\n")  # Use self.ser instead of ser
        print("Sent: stop")
