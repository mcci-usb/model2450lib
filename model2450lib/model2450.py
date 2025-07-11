
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
#     Vinay N, MCCI Corporation May 2025
#
# Revision history:
#    V1.0.1 Wed May 2025 12:05:00   Vinay N
#       Module created
##############################################################################
from model2450lib.serialmodel import SerialDevice
from model2450lib.packetutils import decode_packet, read_packet_from_serial, read_block_frames
import time

class Model2450(SerialDevice):
    def __init__(self, port):
        super().__init__(port)
        self.r_data = []
        self.g_data = []
        self.b_data = []
        self.light_data = []
        self.time_data = []
        self.keep_running = True

    def read_sn(self): 
        return self.send_cmd('sn\r\n')
    
    def read_sn(self): 
        return self.send_cmd('sn\r\n')

    def get_version(self):
        return self.send_cmd('version\r\n')

    def get_color(self):
        return self.send_cmd('color\r\n')

    def get_read(self):
        return self.send_cmd('read\r\n')

    def get_level(self):
        return self.send_cmd('level\r\n')
    
    def set_red(self):
        return self.send_cmd('set red\r\n')
    
    def set_blue(self):
        return self.send_cmd('set blue\r\n')
    
    def set_green(self):
        return self.send_cmd('set green\r\n')
    
    def set_run(self):
        return self.send_text_command('run\r\n')
    
    def set_stop(self):
        return self.send_text_command('stop\r\n')

    def do_reset(self):
        try:
            self.send_command('reset -b\r\n')
            time.sleep(0.1)  # Give time for device to reset
            self.disconnect()  # Close serial port cleanly
        except Exception as e:
            print(f"Ignoring expected error during reset: {e}")
            
    def reset_mode(self):
        try:
            self.send_command('reset\r\n')
            time.sleep(0.1)  # Give time for device to reset
            self.disconnect()  # Close serial port cleanly
        except Exception as e:
            print(f"Ignoring expected error during reset: {e}")

    def set_level(self, value):
        cmd = f'level {value}\r\n'
        return self.send_cmd(cmd)
    
    def get_stream3(self, callback=None):
        """
        Continuously stream data from the device and call the callback with each piece of data.
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
        Sends 'run' command to start blank frames, and automatically sends 'stop' after a specified duration.
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
        Sends 'stop' command to stop the blank frame sequence.
        """
        self.ser.write(b"stop\r\n")  # Use self.ser instead of ser
        print("Sent: stop")
