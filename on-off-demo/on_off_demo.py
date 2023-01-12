# On-Off Demo
# Press one of the buttons to turn the LED on, press again to turn it off.

import time
import picokeypad as keypad

keypad.init()
keypad.set_brightness(1.0)

last_button_states = 0
lit = 0

# lit and button_states are bit arrays. 
# For example, if buttons 16 and 1 are lit, the bit array value would be 0b1000000000000001.

NUM_PADS = keypad.get_num_pads()

for i in range(0, NUM_PADS):
    keypad.illuminate(i, 0x00, 0x00, 0x00)

while True:
    button_states = keypad.get_button_states() # set button_states bit array as updated button states
    if last_button_states != button_states: # if keypad buttons pressed have changed
        last_button_states = button_states # update previous button presses
        
        button = 0
        for i in range(0, NUM_PADS): # cycle through all buttons in keypad
            if button_states & 0x01 > 0: # if button on
                lit = lit ^ (1 << button) # take the complement (invert) if lit bit is already set (on)
            button_states >>= 1 # shift button_states to next button
            button += 1 # increment our button counter to keep decimal track of which button
    
    for i in range(0, NUM_PADS):
        if (lit >> i) & 0x01: # if lit bit array shifted by i is 1
            keypad.illuminate(i, 0x00, 0x20, 0x00) # illuminate key
        else:
            keypad.illuminate(i, 0x00, 0x00, 0x00) # unilluminate key
            
    keypad.update()
    time.sleep(0.05)
