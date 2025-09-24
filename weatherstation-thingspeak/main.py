import time
from machine import Pin
import network
import urequests
import dht

ssid = "Wokwi-GUEST"
password = ''

THINGSPEAK_API_KEY = 'GMRO6XYXC3UJC55V'
THINGSPEAK_URL = 'https://api.thingspeak.com/update'

wlan = network.WLAN(network.STA_IF)
wlan.active(True)
#time.sleep(1)
wlan.connect(ssid, password)

print("Connecting to WiFi", end="")
while not wlan.isconnected():
        print(".", end="")
        time.sleep(0.5)
print("\nConnected!")
print("IP Address:", wlan.ifconfig()[0])

sensor = dht.DHT22(Pin(22))

def send_to_ts(temp):
        if temp is None:
                print("Nothing to send.")
                return
        sdata = 'api_key={}&field1={}'.format(THINGSPEAK_API_KEY,temp)
        #print(sdata)
        try:
                res = urequests.get(
                        THINGSPEAK_URL,
                        data = sdata,
                        headers = { 'Content-Type': 'application/x-www-form-urlencoded' }
                )
                print("ThingSpeak response:", res.status_code, res.text)
                #print(dir(res))
                res.close() # close connection
        except Exception as e:
                print("Error sending: ",e)

while True:
        try:
                sensor.measure()
                temp = sensor.temperature()
                print("Temperature: ", temp, "C")
                send_to_ts(temp)
        except Exception as e:
                print("Error measuring: ",e)
        time.sleep(15)
