from machine import Pin
from utime import sleep

sleep(0.01) # Wait for USB to connect
print("Push the button to turn on LED, release to turn off.")

led = Pin(5, Pin.OUT)
btn = Pin(6, Pin.IN, Pin.PULL_UP)
while True:
  if btn.value(): led.off()
  else: led.on()
  sleep(0.1)
