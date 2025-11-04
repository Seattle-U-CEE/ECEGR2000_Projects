#!/usr/bin/python
# Description: LCD Display Functions
# Author: Eddy Ferre - ferree@seattleu.edu
# Modified from original:
# http://www.tutorials-raspberrypi.de/wp-content/uploads/scripts/hd44780_test.py


from time import sleep
import gpiozero as GPIO

# Assignment of the GPIO pins (adjust if necessary)
LCD_RS = 4
LCD_E = 17
LCD_DATA4 = 18
LCD_DATA5 = 22
LCD_DATA6 = 23
LCD_DATA7 = 24

LCD_WIDTH = 16  # Characters per line
LCD_LINE_1 = 0x80  # Address of the first display line
LCD_LINE_2 = 0xC0  # Address of the second display line
LCD_CHR = True
LCD_CMD = False
E_PULSE = 0.0005
E_DELAY = 0.0005

outputs = {}


def output(pin, state):
    global outputs
    if pin not in outputs:
        print(f'ERROR: Pin {pin} is not allocated')
        return
    if state:
        outputs[pin].on()
    else:
        outputs[pin].off()


def cleanup():
    global outputs
    if outputs == {}:
        return
    for pin in outputs:
        output(pin, False)
        outputs[pin].close()
    outputs = {}


def __lcd_send_byte__(bits, mode):
    output(LCD_RS, mode)
    output(LCD_DATA4, bits & 0x10 == 0x10)
    output(LCD_DATA5, bits & 0x20 == 0x20)
    output(LCD_DATA6, bits & 0x40 == 0x40)
    output(LCD_DATA7, bits & 0x80 == 0x80)
    sleep(E_DELAY)
    output(LCD_E, True)
    sleep(E_PULSE)
    output(LCD_E, False)
    sleep(E_DELAY)
    output(LCD_DATA4, bits & 0x01 == 0x01)
    output(LCD_DATA5, bits & 0x02 == 0x02)
    output(LCD_DATA6, bits & 0x04 == 0x04)
    output(LCD_DATA7, bits & 0x08 == 0x08)
    sleep(E_DELAY)
    output(LCD_E, True)
    sleep(E_PULSE)
    output(LCD_E, False)
    sleep(E_DELAY)


def display_init():
    # initialize
    global outputs
    outputs[LCD_E] = GPIO.LED(LCD_E)
    outputs[LCD_RS] = GPIO.LED(LCD_RS)
    outputs[LCD_DATA4] = GPIO.LED(LCD_DATA4)
    outputs[LCD_DATA5] = GPIO.LED(LCD_DATA5)
    outputs[LCD_DATA6] = GPIO.LED(LCD_DATA6)
    outputs[LCD_DATA7] = GPIO.LED(LCD_DATA7)
    __lcd_send_byte__(0x33, LCD_CMD)
    __lcd_send_byte__(0x32, LCD_CMD)
    __lcd_send_byte__(0x28, LCD_CMD)
    __lcd_send_byte__(0x0C, LCD_CMD)
    __lcd_send_byte__(0x06, LCD_CMD)
    __lcd_send_byte__(0x01, LCD_CMD)
    lcd_message(1, "")
    lcd_message(2, "")


def lcd_message(line, message):
    if line == 1:
        __lcd_send_byte__(LCD_LINE_1, LCD_CMD)
    else:
        __lcd_send_byte__(LCD_LINE_2, LCD_CMD)
    message = message.ljust(LCD_WIDTH, " ")
    for i in range(LCD_WIDTH):
        __lcd_send_byte__(ord(message[i]), LCD_CHR)
    if len(message) > LCD_WIDTH:
        print(f"WARNING: Message line {line} exceeds {LCD_WIDTH} characters")


def lcd_cleanup(final_message1="", final_message2=""):
    lcd_message(1, final_message1)
    lcd_message(2, final_message2)
    cleanup()


if __name__ == '__main__':
    display_init()
    try:
        lcd_message(1, "It seems too")  # Display message on 1st line
        lcd_message(2, "     function :)")  # Display message on 2nd line
        while True:
            sleep(0.2)
    except KeyboardInterrupt:
        print()
        print("Exiting.")
    finally:
        lcd_cleanup()
