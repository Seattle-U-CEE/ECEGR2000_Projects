#!/usr/bin/python
# Description: LCD Display test that repeat typed messages
# Author: Eddy Ferre - ferree@seattleu.edu
# Note: lcdDiplay.py must be in the same folder as this test script

import lcdDisplay

text = ""

try:
    lcdDisplay.display_init()

    text = "Type and I'll"
    lcdDisplay.lcd_message(1, text)
    text = "Repeat:"
    lcdDisplay.lcd_message(2, text)

    print("Type here what you want the LCD to print:")
    while True:
        prev_text = text
        text = input(" > ")
        lcdDisplay.lcd_message(1, prev_text)
        lcdDisplay.lcd_message(2, text)

except KeyboardInterrupt:
    print()
    print("Exiting.")
finally:
    lcdDisplay.lcd_cleanup(text, "bye!")
