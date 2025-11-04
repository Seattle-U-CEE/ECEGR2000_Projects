#!/usr/bin/python
#
# Description: Test code of 3x4 matrix keypad
#
# Author: Eddy Ferre - ferree@seattleu.edu
#


from keypad_4x3 import Keypad
from time import sleep

COLUMN = [5, 6, 13]     # pins 1, 2, 3
ROW = [19, 26, 20, 21]  # pins 4, 5, 6, 7 (8 is NC)

try:
    print("Press keys on your keypad.")
    print(" * = Backspace")
    print(" # = Enter")
    print(" Ctrl+c to quit")
    print()

    # Initialize the keypad class
    kp = Keypad(column=COLUMN, row=ROW)
    kp.start()

    counter = 0
    while True:
        my_digit = kp.get_digit()  # Waits here until key on keypad pressed
        if my_digit == "*":  # Use * as a backspace
            if counter > 0:  # check if keys already printed
                print("\b \b", end="", flush=True)
                counter -= 1
        elif my_digit == "#":  # Use # as enter
            print()
            counter = 0
        else:
            print(my_digit, end="", flush=True)
            counter += 1

except KeyboardInterrupt:
    print()
    print("Exiting")

finally:
    kp.stop()
    sleep(0.2)