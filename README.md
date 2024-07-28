# usbclipboard
Arduino Micro as a clipboard to transfer passwords from "trusted" machine to target.

# Preparation
1. Flash Arduino Micro (Mega32U4) with the code
2. Copy Python script (push.py) to the trusted machine with password manager and create launcher, if needed

# Usage
1. Connect Arduino Micro to USB of trusted machine
2. Open password manager and copy selected password to clipboard
3. Execute python script and get notification "OK: Copied to EEPROM". Now password is saved to EEPROM of Arduino
4. Disconnect Arduino Micro from trusted machine
5. Open desired password prompt on target machine and set cursor to respective text field
6. Connect Arduino Micro to target machine. It will "type" password (as HID device) and remove it from EEPROM

# IMPORTANT
Data is stored in Arduino EEPROM in plain text. It is cleared after each "typing", but between "storing" and "typing" it is in non-volatile memory.
