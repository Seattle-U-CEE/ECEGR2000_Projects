# Enviro pHat

## Install Enviro pHat Software

Open a new terminal, and type the following to enable I2C:
```
sudo raspi-config nonint do_i2c 0
```
Making sure to type 'y' when prompted, execute:
```
sudo apt install python3-envirophat
```
For RaspberryPi 5 and newer, apply the patch, execute:
```
sudo patch -u /usr/lib/python3/dist-packages/envirophat/leds.py -i leds.py.patch
```

## Using the Software

See Pimoroni [Getting started with Enviro pHAT](https://learn.pimoroni.com/article/getting-started-with-enviro-phat#using-the-software)

## color-reader module

This module exercises the color sensor of the Enviro pHat, and continuously returns the closest color name it senses.

- In a terminal session from this folder, execute:
```
python -m color-reader
```
