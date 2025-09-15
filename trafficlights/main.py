from machine import Pin
from utime import sleep

sleep(0.01) # Wait for USB to connect
print("Hello, Pi Pico!")

poll_interval = 0.1 # seconds

# how many cycles to stay in each state
# before auto-transitioning to the next state.
cycles = [32,6,16,4] # [ GREEN, YELLOW, RED, BUZZER ]

pins = [
    Pin(4, Pin.OUT), # GREEN
    Pin(3, Pin.OUT), # YELLOW
    Pin(2, Pin.OUT), # RED
    Pin(28, Pin.OUT) # BUZZER
]
btn = Pin(13, Pin.IN, Pin.PULL_UP)

state = 0 # start in GREEN state
while True:
    btn_down = False
    pins[state].on() # current state led on

    cnt = cycles[state] # set cycle counter based on state
    while cnt:
        # detect button press (negate because pull-up)
        if state==0 and (btn_down := not btn.value()): break
        # if RED toggle buzzer (at a lower rate than poll rate)
        elif state==2 and cnt % cycles[3] == 0: pins[3].toggle()
        sleep(poll_interval)
        cnt -= 1

    pins[3].off() # buzzer off
    pins[state].off() # current state led off

    # state transitions
    state = 1 if btn_down else (state+1 if state<2 else 0)
