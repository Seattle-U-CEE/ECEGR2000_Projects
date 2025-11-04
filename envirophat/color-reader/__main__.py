#!/usr/bin/python
#
# Description: Sample python code to read Enviro pHat colors
#
# Author: Eddy Ferre - ferree@seattleu.edu
#

from math import sqrt
from time import sleep

# Local import
from .BaseColors import base_colors

# Raspberry Pi package
# See: https://learn.pimoroni.com/article/getting-started-with-enviro-phat
# for installation steps
from envirophat import light, leds


def get_color_name(r, g, b):
    key = f"#{r:02X}{g:02X}{b:02X}"
    if key in base_colors:
        return base_colors[key]['color']
    else:
        min_dist = 256.0
        selected_key = None
        for k in base_colors:
            v = base_colors[k]
            dist = sqrt((v['r'] - r) ** 2 + (v['g'] - g) ** 2 + (
                        v['b'] - b) ** 2)
            if dist < min_dist:
                min_dist = dist
                selected_key = k
        return base_colors[selected_key]['color']


def main():
    try:
        leds.on()
        while True:
            r, g, b = light.rgb()
            print(f'  detecting : {get_color_name(r, g, b)}                       ',
                  end='\r')
            sleep(0.2)

    except KeyboardInterrupt:
        print()
        print("Exiting")
    except Exception as e:
        print(f'Exception: {e}')
    finally:
        leds.off()


if __name__ == '__main__':
    main()
