# pyPLCD
Control the Raspberry Pi with a 16x2 Display Shield

## Display
![Display Shield](http://www.adafruit.com/images/large/1110green_LRG.jpg)
[Adafruit 16x2 Character LCD + Keypad for Raspberry Pi](http://www.adafruit.com/products/1110)

### 

## Setup

### Python Modules
[Adafruit Repository](https://github.com/adafruit/Adafruit-Raspberry-Pi-Python-Code/): CharLCDPlate, I2C & MCP230xx

### Arch
...

### Debian
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
 - Filesystems
 - Memory
 - Network Info
 - Kernel
- Control
 - Shutdown/Reboot
- 3rd Party Support
 - [SlyPi](https://github.com/Xtrato/Slypi)
 - [Adafruit Python-WiFi-Radio](https://github.com/adafruit/Python-WiFi-Radio)
 
 
## ToDo 
- Network Control
 - set ip, route...
 - WiFi
 - AccesPoints

- Software Control
  - Services (sshd, ftp, http...)
  - XBMC Controls

- Log Parser
 - Full Log
 - Errors & Warnings
 - special Keywords

- Security
 - Sniffer
 - NMAP
 - Rogue AP
 - Reverse Tunnel
 - Proxy
 - SET
 - BruteForce
 - [FruityWifi](https://github.com/xtr4nge/FruityWifi) GUI/Controls

## notice
This is my first Python project, it should help me to learn Python...

Any recommendations/tipps are welcome :)