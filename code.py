# RgbKeypadStringMacro.py 2022-11-24 Jim Fred
#
# Derived from SPDX-FileCopyrightText: 2021 Sandy Macdonald
# A simple example of how to set up a keymap and HID keyboard on Keybow 2040.
# Expects KeyStrings.py containing key_strings, as string array.
#
# Connect RgbKeypad to a computer, as you would with a regular USB keyboard.
#
# Required libraries in the `lib` folder on your `CIRCUITPY` drive:
# - `pmk` folder
# - adafruit_hid CircuitPython library

from pmk import PMK
# from pmk.platform.keybow2040 import Keybow2040 as Hardware          # for Keybow 2040
from pmk.platform.rgbkeypadbase import RGBKeypadBase as Hardware  # for Pico RGB Keypad Base
from pmk.platform.rgbkeypadbase import _ROTATED as KeypadRotation # Seems to be needed for RGB Keypad so that key indexes match silkscreens.

import usb_hid
from adafruit_hid.keyboard import Keyboard
from adafruit_hid.keyboard_layout_us import KeyboardLayoutUS
from adafruit_hid.keycode import Keycode
import KeyStrings # My KeyString.py config file.


# Set up Keybow
keybow = PMK(Hardware())
keys = keybow.keys

# Set up the keyboard and layout
keyboard = Keyboard(usb_hid.devices)
layout = KeyboardLayoutUS(keyboard)

## layout.write('A$%bc\n')

# A map of keycodes that will be mapped sequentially to each of the keys, 0-15
key_strings = KeyStrings.key_strings
if key_strings is None:
    key_strings = [
        'Zero\n',  # key 0 
        'One\n',   # key 1
        'Two\n',   # key 2
        'Three\n', # key 3
        'Four\n',  # key 4
        'Five\n',  # key 5
        'Six\n',   # key 6
        'Seven\n', # key 7
        'Eight\n', # key 8
        'Nine\n',  # key 9
        'A',     # key A
        'B',     # key B
        'C',     # key C
        'D',     # key D
        'E',     # key E
        'F\n',     # key F
    ]

# The colour to set the keys when pressed and released.
colour_key_press = (0, 255, 0)
colour_key_pause = (0,1,0)
colour_key_release = (1,1,1)

## send_str('asdfASDF')

# Attach handler functions to all of the keys
for key in keys:
    key.set_led(*colour_key_release)
    
    # A press handler that sends the keycode and turns on the LED
    @keybow.on_press(key)
    def press_handler(key):
        key.set_led(*colour_key_press)
        key_number = KeypadRotation[key.number]  # rotate indexes.
        send_string = key_strings[key_number]    # get the string
        layout.write(send_string)                # send the string to the PC.
        key.set_led(*colour_key_pause)

    # A release handler that turns off the LED
    @keybow.on_release(key)
    def release_handler(key):
        key.set_led(*colour_key_release)
            

while True:
    keybow.update()  # Always remember to call keybow.update()!
    
    