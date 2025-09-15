from machine import Pin
from utime import sleep

sleep(0.01) # Wait for USB to connect
print(
    "RasPi GPIO pins are 3.3V. "
    "Assuming 2.1V forward voltage for the LED, "
    "a 120 Ohm resistor will limit the current to 10mA. "
    "(3.3V - 2.1V) / 120Ohm = 10mA")

led = Pin(5, Pin.OUT)
while True:
  led.toggle()
  sleep(0.5)
