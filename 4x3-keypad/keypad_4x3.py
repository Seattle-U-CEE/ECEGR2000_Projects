#!/usr/bin/python
#
# Description: Python Library for 3x4 matrix keypad using
# 7 GPIO pins on the Raspberry Pi. Pins may be changed on instantiation
#
# Author: Eddy Ferre - ferree@seattleu.edu
#

import gpiozero as GPIO
from threading import Thread
from time import sleep


# Global Variables
outputs = {}
inputs = {}

def output(pin, state):
    global outputs
    if pin not in outputs:
        print(f'ERROR: Pin {pin} is not allocated')
        return
    if state:
        outputs[pin].on()
    else:
        outputs[pin].off()


def input(pin):
    global inputs
    if pin not in inputs:
        print(f'ERROR: Pin {pin} is not allocated')
        return None
    return inputs[pin].is_pressed


def setup_output(pin):
    global outputs
    global inputs
    if pin in inputs:
        inputs[pin].close()
        del inputs[pin]
    if pin not in outputs:
        outputs[pin] = GPIO.LED(pin)


def setup_input(pin, pull_up=True):
    global outputs
    global inputs
    if pin in outputs:
        outputs[pin].close()
        del outputs[pin]
    if pin not in inputs:
        inputs[pin] = GPIO.Button(pin, pull_up=pull_up)


def cleanup():
    global outputs
    global inputs
    for pin in outputs:
        output(pin, False)
        outputs[pin].close()
    outputs = {}
    for pin in inputs:
        inputs[pin].close()
    inputs = {}


class Keypad(Thread):
    # CONSTANTS   
    KEYPAD = [
        ["1", "2", "3"],
        ["4", "5", "6"],
        ["7", "8", "9"],
        ["*", "0", "#"]
    ]
    # Default GPIO Pins
    COLUMN = [5, 6, 13]     # pins 1, 2, 3
    ROW = [19, 26, 20, 21]  # pins 4, 5, 6, 7 (8 is NC)

    def __init__(self, column=None, row=None):
        super().__init__()
        if column is None:
            self.column = self.COLUMN
        elif type(column) == list and len(column) == 3:
            self.column = column
        else:
            raise ValueError("column argument of Keypad must be list length 3")
        if row is None:
            self.row = self.ROW
        elif type(row) == list and len(row) == 4:
            self.row = row
        else:
            raise ValueError("row argument of Keypad must be list length 4")

        self.digit_ready = False
        self.last_digit = None
        self.is_stopped = False

    # Thread run method, invoked by instance 'start()'
    def run(self):
        while not self.is_stopped:
            self.__get_key()
            sleep(0.1)

    # Get the latest digit pressed. Wait here until digit is depressed
    def get_digit(self):
        while True:
            if self.digit_ready and self.last_digit is not None:
                self.digit_ready = False
                return self.last_digit
            sleep(0.1)

    # Internal method to set and read the GPIOs
    def __get_key(self):
        # Set all columns as output low
        for j in range(len(self.column)):
            setup_output(self.column[j])
            output(self.column[j], False)

        # Set all rows as input
        for i in range(len(self.row)):
            setup_input(self.row[i], True)

        # Scan rows for pushed key/button
        # A valid key press should set "row_val"  between 0 and 3.
        row_val = -1
        for i in range(len(self.row)):
            if input(self.row[i]):
                row_val = i

        # if row_val is not 0 through 3 then no button was pressed and
        # we can exit
        if row_val < 0 or row_val > 3:
            self.last_digit = None
            self.digit_ready = False
            self.__exit()
            return

        # Convert columns to input
        for j in range(len(self.column)):
            setup_input(self.column[j], False)

        # Switch the i-th row found from scan to output
        setup_output(self.row[row_val])
        output(self.row[row_val], True)

        # Scan columns for still-pushed key/button
        # A valid key press should set "col_val"  between 0 and 2.
        col_val = -1
        for j in range(len(self.column)):
            if input(self.column[j]):
                col_val = j

        # if col_val is not 0 through 2 then no button was pressed
        # and we can exit
        if col_val < 0 or col_val > 2:
            self.__exit()
            return

        # Set the value of the key pressed
        self.__exit()

        if not self.digit_ready and self.last_digit is None:
            self.digit_ready = True
            self.last_digit = self.KEYPAD[row_val][col_val]

    # Reinitialize all rows and columns as input at exit
    def __exit(self):
        for i in range(len(self.row)):
            setup_input(self.row[i], True)
        for j in range(len(self.column)):
            setup_input(self.column[j], True)

    # Stop the thread
    def stop(self):
        self.is_stopped = True
        try:
            cleanup()
        except:
            pass
