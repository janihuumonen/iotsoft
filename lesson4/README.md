## IoT pipeline
sensor.py	- micropython pico w sensor, simulated in wokwi
server.ts	- deno server & sqlite database
index.html	- dashboard

pico sends data as POST request, server writes it to the database and forwards it to dashboard via websocket connections
dashboard get all data collected so far when opening a websocket connection and gets updates as new data is collected

### TODO
- dashboard linechart
