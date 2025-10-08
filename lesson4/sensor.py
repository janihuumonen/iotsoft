import time
from machine import Pin
import network
import urequests
import dht

ssid = "Wokwi-GUEST"
password = ''

DEV_ID = 'wokwipico'
ENDPOINT_URL = 'http://janih.fi:3000'

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

def send_to_ts(temp,humi):
        if temp is None or humi is None:
                print("Nothing to send.")
                return
        sdata = 'devID={}&temp={}&humi={}'.format(DEV_ID,temp,humi)
        print(sdata)
        try:
                res = urequests.post(
                        ENDPOINT_URL,
                        data = sdata,
                        headers = { 'Content-Type': 'application/x-www-form-urlencoded' }
                )
                print("Response:", res.status_code, res.text)
                #print(dir(res))
                res.close() # close connection
        except Exception as e:
                print("Error sending: ",e)

while True:
        try:
                sensor.measure()
                temp = sensor.temperature()
                humi = sensor.humidity()
                print("Temperature: ", temp, "C")
                send_to_ts(temp,humi)
        except Exception as e:
                print("Error measuring: ",e)
        time.sleep(15)

