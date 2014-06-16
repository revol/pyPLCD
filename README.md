# pyPLCD
Control the Raspberry Pi with a 16x2 Display

## Display
![Display Shield](http://www.adafruit.com/images/large/1110green_LRG.jpg)
[Adafruit 16x2 Character LCD + Keypad for Raspberry Pi](http://www.adafruit.com/products/1110)

## Python Modules
https://github.com/adafruit/Adafruit-Raspberry-Pi-Python-Code/tree/master/Adafruit_CharLCDPlate

## Arch
...

## Debian Setup
```bash
echo "i2c-bcm2708
i2c-dev" >> /etc/modules

apt-get install python-dev python-rpi.gpio python-smbus i2c-tools
```

## Features
- Display Status
 - Time
 - Load
 - Temperature
 - Network Info
 - Kernel
- Control
 - Shutdown/Reboot
- 3rd Party Support
 - [SlyPi](https://github.com/Xtrato/Slypi)
 - [Adafruit Python-WiFi-Radio](https://github.com/adafruit/Python-WiFi-Radio)
 
 
## ToDo
- Display Status
 - Space
- Log Parser
 - Full Log
 - Errors & Warnings
 - special Keywords
- Control
 - Network
  - set ip
  - WiFi
   - AccesPoints
 - Software
  - Services (sshd, ftp, http...)
  - XBMC Control
  - Security
   - Sniffer
   - NMAP
   - Rogue AP
   - Reverse Tunnel
   - Proxy
   - FakeSites...
   - BruteForce


## notice
This is my first python project
It should help me to learn Python...
Any recommendations/tipps are welcome :)
