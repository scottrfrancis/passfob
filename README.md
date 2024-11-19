# Passfob - an insecure password keyfob

A simple [CircuitPython](https://learn.adafruit.com/welcome-to-circuitpython/overview) app to help me enter passwords using the Adafruit [Circuit Playground Express](https://www.adafruit.com/product/3333) (CPX).

### Motivation

If you have some environment where you need to 

* change passwords frequently
* have long, complex passwords
* have to enter them A LOT

This project allows you to save the **_CLEAR TEXT_** password on the CPX and enter it when you push the 'A' Button.

**_WARNING: THIS IS HIGHLY INSECURE AS THE PASSWORD IS STORED AS PLAIN TEXT AND CAN EASILY BE RECOVERED. NO AUTHENTICATION IS DONE FOR THE BUTTON PUSH. ANYONE WHO HAS PHYSICAL POSSESSION OF THE CPX CAN USE THE PASSWORD_**

## Setup

With a Circuit Playground Express

1. Update to the latest version of [CircuitPython](https://circuitpython.org/board/circuitplayground_express/).  _This project was developed with verion 9.2.0_

2. Copy the file `code.py` to the CPX.

3. Set your password to the file `.password` on the CPX.  It may be easiest to do this using a terminal program.

**_NB_**: some systems may restrict this kind of access and/or block mounting the CPX as read-write. In which case, you may need to do this setup on another computer.

## Usage

1. connect the CPX to the system you need to log in to.
2. the CPX pixels will flash briefly, then blank
3. If all the pixels are RED, no password file was found.  It is normal for there to be a red flash when first powering on the CPX.
4. the small red led (opposite the green, power led) functions as a hearbeat to let you know the CPX is alive and the program running.
5. When the password has been found and loaded, the pixels will rotate around clockwise in green.
6. Push the 'A' Button (aka `D4` to the left of the reset button) -- the pixels will blank and the hearbeat will flash rapidly while the button is held.
7. When the 'A' Button is released, the password will be spooled out on char at a time and the pixels will rotate in BLUE.
8. The pixels will then flash in RED again before reloading the password and giving rotating green dots.

## Notes

* Since the CPX enumerates as a keyboard, this device can also be used to 'wake' a sleeping system.

* A nice add-on that maybe I'll do some day is to store several passwords and select them with the touch pads.

* Setting a 'pin' with the touchpads would also be a good idea.