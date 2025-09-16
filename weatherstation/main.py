from machine import Pin
import utime
from dht import DHT22 

utime.sleep(0.01) # Wait for USB to connect
print("Measures temperature and humidity.")

sensor = DHT22(Pin(22))

while True:
    sensor.measure()
    temp = sensor.temperature()
    humidity = sensor.humidity()
    print('Temperature: %2.2f C' %temp)
    print('Humidity: %2.2f %%' %humidity)
    utime.sleep(1)
