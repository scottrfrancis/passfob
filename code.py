# Passfob
#
# This code is for the Circuit Playground Express
# Send a stored password (from a file) to a computer over USB
# when a button is pressed.
#
# The password is stored in a file called ".password" on the
# Circuit Playground Express.
#
# The password is sent as a keyboard input to the computer.
# The password is sent as a series of key presses, not as a
# single string.
#
# Reference: https://circuitpython.org/board/circuitplayground_express/
#

import random
from adafruit_circuitplayground import cp
from adafruit_hid.keyboard import Keyboard
from adafruit_hid.keyboard_layout_us import KeyboardLayoutUS
from adafruit_hid.keycode import Keycode  
from adafruit_hid.mouse import Mouse
import time
import usb_hid


kbd = Keyboard(usb_hid.devices)
layout = KeyboardLayoutUS(kbd)

mouse = Mouse(usb_hid.devices)

def send_key(key):
    global layout, kbd

    codes = layout.keycodes(key)
    kbd.send(*codes)

def send_enter():
    global kbd

    kbd.send(Keycode.ENTER)

def button_pressed():
    return cp.button_a

last_move = time.monotonic()
move_interval = random.randint(5, 300)
def wiggle_mouse():
    global mouse, last_move, move_interval

    if time.monotonic() - last_move > move_interval:
        last_move = time.monotonic()
        move_interval = random.randint(5, 300)

        x = random.randint(-800, 800)
        y = random.randint(-800, 800)
        mouse.move(x, y)

override_switch = False
def switch_active():
    global override_switch
    return cp.switch and not override_switch
# only fiddle witht the LED if it is not active
def set_led_on():
    cp.red_led = switch_active()

def set_led_off():
    cp.red_led = False

def toggle_led():
    # cp.red_led = switch_active() and not cp.red_led 
    cp.red_led = not cp.red_led 
set_led_on()

pixel_cursor = 0

cp.pixels.brightness = 0.1

red = (255, 0, 0)
green = (0, 255, 0)
blue = (0, 0, 255)
black = (0, 0, 0)
white = (255, 255, 255)

def set_all_pixels(color):
    if not switch_active():
        color = black
    cp.pixels.fill(color)
    cp.pixels.show()
set_all_pixels(red)

def set_pixel(index, color):
    if not switch_active():
        color = black
    cp.pixels[index] = color
    cp.pixels.show()

def rotate_pixels(color):
    global pixel_cursor

    set_pixel(pixel_cursor, black)
    pixel_cursor -= 1
    if pixel_cursor < 0:
        pixel_cursor = 9
    set_pixel(pixel_cursor, color)
    cp.pixels.show()

# list of possible states
states = {
    "IDLE": 0,
    "WAIT_FOR_PRESS": 1,
    "SENDING_PASSWORD": 2,
    "WAIT_FOR_RELEASE": 3,
    "NOT_READY": 4,
}
state = states["NOT_READY"]


# tick timing -- default to 100 mS, but can be adjusted
# as needed -- say for spooling out the key presses
tick = 0.1

# read the password from the file
password = None
# password is pop'd off the front of the list as it is sent
# when the password is empty, call the read_password() function
# to reload it from the file
def read_password():
    global password

    password_file = ".password"
    try:
        with open(password_file, "r") as file:
            password = file.read().strip()
    except OSError as e:
        password = None
    # add a return to enter the password

def do_work():
    global password, state, tick, override_switch

    # take action based on current state
    toggle_led()
    if state == states["IDLE"]:
        # slow flash the LED
        tick = 0.5
        # set_all_pixels(green)
        rotate_pixels(green)
    elif state == states["NOT_READY"]:
        set_all_pixels(red)
        # try to read it again
        read_password()
    elif state == states["WAIT_FOR_RELEASE"]:
        # fast flash the LED
        tick = 0.05
        set_all_pixels(black)
    elif state == states["SENDING_PASSWORD"]:
        override_switch = True
        rotate_pixels(blue)
        # send the next key press -- quickly
        if password:
            key = password[0]
            send_key(key)

            # remove the key from the password
            password = password[1:]
            if not password:
                # send a ENTER key to finish the password
                send_enter()
                override_switch = False
        tick = 0.1

    # detect state -- order is important here
    # advance to next state if conditions are met
    if not password:
        state = states["NOT_READY"]
    elif button_pressed():
        # wait for the button to be released
        state = states["WAIT_FOR_RELEASE"]
    elif (state == states["WAIT_FOR_RELEASE"]):
        # button was released
        state = states["SENDING_PASSWORD"]
    elif state == states["SENDING_PASSWORD"]:
        # just keep going until password spooled out
        pass
    else:
        state = states["IDLE"]

    # if switch is NOT active, wiggle the mouse
    if not switch_active():
        override_switch = True
        set_all_pixels(green)
        wiggle_mouse()
        time.sleep(0.1)
        set_all_pixels(black)
        override_switch = False


# print("Passfob ready")
while True:
    time.sleep(tick)
    do_work()
