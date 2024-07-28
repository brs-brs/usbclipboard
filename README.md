# Project description: usbclipboard

Hardware device for easy password transfer from an air-gapped trusted machine with a password manager to a target device. For the "source" device, it looks like a UART terminal (9600 baud rate), which expects a "\n"-terminated password string. For the "target" device, it looks like an HID keyboard.

## Preparation

1. Flash an Arduino Micro (Mega32U4) with the appropriate firmware.
2. Copy the Python script (`push.py`) to the trusted machine with the password manager and adjust the serial device name, if needed.

## Usage

1. Connect the Arduino Micro to the trusted machine via USB.
2. Open the password manager and copy the selected password to the clipboard.
3. Execute the Python script and wait for the notification "OK: Copied to EEPROM". The password is now saved to the EEPROM of the Arduino.
4. Disconnect the Arduino Micro from the trusted machine.
5. Open the desired password prompt on the target machine and place the cursor in the respective text field.
6. Connect the Arduino Micro to the target machine. It will "type" the password (as an HID device) and then remove it from the EEPROM.

## IMPORTANT

Data is stored in the Arduino EEPROM in plain text. It is cleared after each "typing", but between "storing" and "typing" it is in non-volatile memory.
