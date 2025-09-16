from machine import Pin
import utime

utime.sleep(0.01) # Wait for USB to connect
print("LED is on when movement is detected (and stays on for 5s after detection).")

led = Pin(5, Pin.OUT)
pir = Pin(22, Pin.IN, Pin.PULL_DOWN)

def pir_cb(pin):
    led.value(pin.value())
    print("Movement","detected" if pin.value() else "ended")

pir.irq(
    handler = pir_cb,
    trigger = Pin.IRQ_FALLING | Pin.IRQ_RISING )

# idle
while True:
    utime.sleep(1)
