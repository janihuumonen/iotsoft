from machine import Pin, Timer
import utime
from random import randint

utime.sleep(0.01) # Wait for USB to connect
print("Push the button when the LED turns off!")

led = Pin(5, Pin.OUT)
btn = Pin(6, Pin.IN, Pin.PULL_UP)

timer = Timer()
ticking = False
tick = 0

def new_round():
    global ticking
    timer.init(
        mode = Timer.ONE_SHOT,
        period = randint(500,1500),
        callback = timer_cb )
    ticking = True
    led.value(1)

def timer_cb(t):
    global ticking,tick
    led.value(0)
    tick = utime.ticks_ms() # save current time
    ticking = False

def btn_cb(p):
    if ticking: return # ignore button when timer is running
    # print reaction time and start a new round
    print(str( utime.ticks_diff(utime.ticks_ms(), tick) ) + " ms")
    new_round()

btn.irq(
    handler = btn_cb,
    trigger = Pin.IRQ_FALLING )

new_round() # start

# idle
while True:
    utime.sleep(1)
