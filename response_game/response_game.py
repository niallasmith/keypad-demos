import time
import picokeypad as keypad
import random
import math

keypad.init()
keypad.set_brightness(1.0)

last_button_states = 0

# lit and button_states are bit arrays. 
# For example, if buttons 16 and 1 are lit, the bit array value would be 0b1000000000000001.

NUM_PADS = keypad.get_num_pads()

while True:
    time.sleep(2)
    response_time_total = 0
    num_rounds = 15
    for games in range(0,num_rounds-1):

        time.sleep(random.random())
        random_button = random.randint(0,15)

        lit = 0
        lit = lit | (1 << random_button)
        
        for i in range(0, NUM_PADS):
            if (lit >> i) & 0x01: # if lit bit array shifted by i is 1
                keypad.illuminate(i, 0x20, 0, 0) # illuminate key
            else:
                keypad.illuminate(i, 0x00, 0x00, 0x00) # unilluminate key
        start = time.ticks_ms()
        
        while True: # remain in loop until user presses correct button, breaking from loop
            keypad.update()
            button_states = keypad.get_button_states() # set button_states bit array as updated button states
            if last_button_states != button_states:
                last_button_states = button_states # update previous button presses
                
                if button_states & (1 << lit_button) > 0:
                    break
        end = time.ticks_ms() 
        
        keypad.illuminate(random_button, 0x00, 0x00, 0x00) # unilluminate key
            
        response_time_total += (end - start) # calculate how long response took and add to running total
    
    print(math.floor(response_time_total / num_rounds), "milliseconds") # display users average response time in ms

    # post game code, display green button to play again when pressed
    while True: # remain in loop until user plays again, breaking from loop
        keypad.illuminate(0, 0x00, 0x20, 0x00) # illuminate green
        keypad.update()
        button_states = keypad.get_button_states()
        if last_button_states != button_states: # if keypad has been pressed
            last_button_states = button_states # update previous button presses
            if button_states & 0x01 > 0: # if button 1 has been pressed to play again
                break
