
Not so smart home managment app.
Work in progress.
Purpose is learing python, flask, html/css, sql and some digital electronics basics.

Python/flask
Raspberry/Arduino


Hardware so far:
- Raspberry Pi 2B
- arduino nano
- wifi dongle
- speakers for media
- 2 relay modules and modified extension wall socket
#- 2 DS18B20 sensors
- 1 DS18B20 sensor
#- DHT11 sensor
- IR receiver & remote
- 7-segment max7219 display


Requirements:
Main app:
- python3
- Flask

Media playing:
- VLC
- vlc-python

For communication with Arduino by USB/serial:
- pyserial
#- requests - for sending POSTs to main app
- selectors - for 

For InfraRed communication by remote with Raspberry:
- ir-keytable - for managing Linux IR
- evdev - for catching rc events
#- requests - for sending POSTs to main app

For 7-segment display:
- max7219 

Arduino libs:
- OneWire
- DallasTemperature
#- dht

Useful guide for enabling IR on Raspberry:
https://github.com/gordonturner/ControlKit/blob/master/Raspbian%20Setup%20and%20Configure%20IR.md

TODO:
- unpluing arduino causes an error, since dev file is gone
- ir-keytable confiration on boot
- make main app independent local-webapp, all options as optional modules
\- sending sensors data to main app by POSTs
\- logging to database and displaying sensors readings in app and so on, almost done.
- get those temperature charts working properly
- 7-segment display for common night clock, diplaying easly visible informations. 
max7219 7-segment display, as I can't get the TM1637 ones to work.
Perhaps becuase of:
https://www.eluke.nl/2018/03/23/fixed-tm1637-led-display-not-working/
https://www.picprojects.org/archives/347
As there seem to be two 103(10 nano)capacitors on my modules.
- get some sensors really "outside" already and send data to arduino wireless
- wireless relay switching of under-ceiling lamp
- hardcoded configuration is bad, move whatever you can to settings tab in the webapp
