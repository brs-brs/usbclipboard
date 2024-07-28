#!/usr/bin/env python3

import pyperclip
import serial
import time
import subprocess

SERIAL_DEVICE = '/dev/ttyACM0'

def send_notification(message):
    subprocess.run(['notify-send', message])

def contains_non_ascii(s):
    return any(ord(char) >= 128 for char in s)

def handshake(ser):
    try:
        ser.write("######CLIP?######\n".encode('ascii'))  # unlikely to be a password
        time.sleep(0.05)
        reply = ser.read(5)
        if reply.decode('ascii') != "board":
            send_notification("ERR: handshake failed. Wrong serial device?")
            return -1
        return 0

    except serial.SerialException as e:
        send_notification(f"ERR: serial communication error: {e}")
        return -1

def send_clipboard_to_serial():
    clipboard_content = pyperclip.paste()
    if not clipboard_content:
        send_notification("ERR: Clipboard is empty or exceeds 50 characters.")
        return
    if len(clipboard_content) > 49:
        send_notification("ERR: Clipboard string is too long")
    if contains_non_ascii(clipboard_content):
        send_notification("ERR: Clipboard contains non-ASCII characters.")
        return

    try:
        ascii_content = clipboard_content.encode('ascii', 'ignore').decode('ascii')
        with serial.Serial(SERIAL_DEVICE, 9600, timeout=0.5) as ser:
            if handshake(ser) != 0:
                return
            ser.write((ascii_content + '\n').encode('ascii'))
            reply = ser.read(5)
            if not reply:
                send_notification("ERR: no ACK from device")
                return
            if reply.decode('ascii') == "gotit":
                send_notification("OK")
            else:
                send_notification("ERR: wrong ACK from device")
    except serial.SerialException as e:
        send_notification(f"ERR: {e}")

if __name__ == "__main__":
    send_clipboard_to_serial()
