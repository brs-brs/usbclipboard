#!/usr/bin/env python3

import pyperclip
import serial
import time
import subprocess

def send_notification(message):
    subprocess.run(['notify-send', message])

def contains_non_ascii(s):
    return any(ord(char) >= 128 for char in s)

def send_clipboard_to_serial():
    clipboard_content = pyperclip.paste()
    if clipboard_content and len(clipboard_content) <= 50:
        if contains_non_ascii(clipboard_content):
            send_notification("Clipboard contains non-ASCII characters.")
            return
        try:
            ascii_content = clipboard_content.encode('ascii', 'ignore').decode('ascii')
            with serial.Serial('/dev/ttyACM0', 9600, timeout=0.2) as ser:
                time.sleep(0.05)
                ser.write((ascii_content + '\n').encode('ascii'))
                send_notification("Sent to ttyACM0.")
        except serial.SerialException as e:
            send_notification(f"Error: {e}")
    else:
        send_notification("Clipboard is either empty or exceeds 50 characters.")

if __name__ == "__main__":
    send_clipboard_to_serial()
