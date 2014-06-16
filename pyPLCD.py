#!/usr/bin/python
# pyPLCD

PiPhi = "/opt/Python-WiFi-Radio/PiPhi.py"   # Python-WiFi-Radio
SlyPi = "/opt/slypi/slypi.py"               # SlyPi

import subprocess
import time
import os
from Adafruit_CharLCDPlate import Adafruit_CharLCDPlate
from random import randint
from time import sleep

# version info
version = ('0.0.1', '2014-02-02')

# Initialize the LCD plate.  Should auto-detect correct I2C bus.  If not,
# pass '0' for early 256 MB Model B boards or '1' for all later versions
lcd = Adafruit_CharLCDPlate()

# Menus
menu_list = [("Clock", "show_clock()"),
             ("System Info",
              [("CPU", "sys_info('cpu')"),
               ("Memory", "sys_info('mem')"),
               ("Disk", "sys_info('df')"),
               ("Network",
                [("soon (tm)", "net_info()"),
                 ("Hostname", "sys_info('H')")]),
               ("Kernel", "sys_info('kern')"),
               ("pyPLCD Version", "startup()")]),
             ("Services",
              [("networking", "ctl_service('networking', state='restart')"),
               ("ssh", "ctl_service('ssh')")]),
             ("External",
              [("Internet Radio", "run_external(PiPhi)"),
               ("SlyPi", "run_external(SlyPi)"),
               ("Test", "run_external('/no/valid/path')")]),
             ("Reboot", "shutdown('r')"),
             ("Shutdown", "shutdown('h')"),
             ("Exit pyPLCD", "shutdown('x')")]


############
# OBJECTS
############

# Startup Message
def startup():
    lcd.clear()
    lcd.backlight(lcd.GREEN)
    lcd.message(" pyPLCD v{}\n reV {}".format(version[0], version[1]))
    sleep(2)
    clean_display()


# Clock
def show_clock():
    random_bg_color()
    while True:
        lcd.clear()
        now = time.ctime().split()
        lcd.message("    {}\n{}  {} {} {}".format(now[3], now[0], now[1], now[2], now[4]))
        sleep(1)
        # exit
        if lcd.buttonPressed(lcd.SELECT):
            clean_display()
            break


# System Information
def sys_info(x):
    lcd.backlight(lcd.VIOLET)
    if x == "H":                    # Hostname
        show_message("Hostname:\n{}".format(run_command("uname -n")), "GREEN")
    elif x == "kern":               # Kernel Version
        show_message("Kernel:\n{}".format(run_command("uname -rm")))
    elif x == "cpu":                # CPU
        cpu = int(readfile("/sys/devices/system/cpu/cpu0/cpufreq/scaling_max_freq")) / 1000
        while True:
            temp = float(readfile("/sys/class/thermal/thermal_zone0/temp")) / 1000
            freq = int(readfile("/sys/devices/system/cpu/cpu0/cpufreq/scaling_cur_freq")) / 1000
            top = (run_command("top -b -n1"))[2].split()                                    # FIXME Not working CPULoad
            load = float(top[1]) + float(top[3])
            if temp <= 45.0:
                set_color("GREEN")
            elif temp >= 55.0:
                set_color("RED")
            else:
                set_color("YELLOW")
            lcd.clear()
            lcd.message(" {} / {} MHz\n {}'C   {}%".format(freq, cpu, format(temp, '.1f'), format(load, '.1f')))
            # lcd.message("Temp: {} 'C\n{}/{}MHz  %{}".format(format(temp, '.0f'), freq, format(load, '3.0f')))
            sleep(1)
            if lcd.buttonPressed(lcd.SELECT):
                clean_display()
                break
    elif x == "mem":                # Memory
        mem = (readfile("/proc/meminfo"))
        memtotal = float(mem[0].split()[1]) / 1024
        memfree = float(mem[1].split()[1]) / 1024
        while True:
            lcd.clear()
            set_color("VIOLET")
            lcd.message("Mem:  {} MB\nFree: {} MB".format(format(memtotal, '.2f'), format(memfree, '.2f')))
            sleep(1)
            if lcd.buttonPressed(lcd.SELECT):
                clean_display()
                break
    # TODO Rewrite as dictionary (like network info)
    elif x == "df":                 # Disk
        df = (run_command("df -h"))
        disk = []
        for line in df:
            if "/dev/" in line:
                disk.append(line.split())
        # Menu  FIXME Need Menu with left/right moving
        for item in disk:
            while True:
                lcd.clear()
                set_color("VIOLET")
                lcd.message("{}  {}\n  {} / {}".format(item[5], item[4], item[2], item[1]))
                sleep(0.5)
                while lcd.buttonPressed(lcd.SELECT) != 1:
                    pass
                break


# Service Control
def ctl_service(service, state="status"):
    # init.d or system.d ?
    if os.path.isdir("/etc/init.d"):
        cmd = "service {} {}".format(service, state)
    else:
        cmd = "systemctl {} {}".format(state, service)
    print run_command(cmd)


# Network
def net_info():
    # get interface info
    interface = {}
    iflist = run_command("ip addr")
    for line in iflist:
        if line[1] == ":":
            ifname = line.split()[1][:-1]
            interface[ifname] = {}
        elif "link/ether" in line:
            interface[ifname]["mac"] = line.split()[1]
        elif "inet " in line:
            interface[ifname]["ip"] = line.split()[1].split("/")[0]
    del interface["lo"]

    # Menu                                                                      # FIXME Need Menu with left/right moving
    for iface in interface:
        while True:
            for item in interface[iface]:
                while True:
                    lcd.clear()
                    set_color("VIOLET")
                    lcd.message("{}:  {}\n{}".format(iface, item, interface[iface][item]))
                    sleep(0.5)
                    while lcd.buttonPressed(lcd.SELECT) != 1:
                        pass
                    break
            break


# run external scripts
def run_external(path):
    clean_display()
    if os.path.isfile(path):
        sleep(0.5)
        proc = subprocess.Popen(['python', path])
        while lcd.buttonPressed(lcd.LEFT) != 1 or lcd.buttonPressed(lcd.RIGHT) != 1:
            pass
        proc.kill()
    else:
        lcd.backlight(lcd.RED)
        lcd.message("Not Found!")
        sleep(2)


# Shutdown/Reboot
def shutdown(x):
    lcd.clear()
    lcd.backlight(lcd.RED)

    if x == 'r':
        bash = 'reboot'
        lcd.message("?    REBOOT    ?")
    elif x == 'h':
        bash = 'shutdown -h now'
        lcd.message("?   SHUTDOWN   ?")
    elif x == 'x':
        lcd.message("?     EXIT     ?")

    lcd.message("\n UP=YES DOWN=NO ")
    while True:
        sleep(0.1)
        if lcd.buttonPressed(lcd.UP):
            lcd.message("\n    Bye  Bye    ")
            sleep(1)
            if x == 'x':    # Exit
                clean_display()
                exit(0)
            else:           # Shutdown/Reboot
                subprocess.Popen(bash.split())
                clean_display()
        # Cancel
        elif lcd.buttonPressed(lcd.DOWN):
            clean_display()
            sleep(0.5)
            break


############
# FRAMEWORK
############

# Clean Display
def clean_display():
    lcd.clear()
    lcd.backlight(lcd.OFF)
    sleep(0.2)


# show message
def show_message(message, color="VIOLET"):
    lcd.clear()
    set_color(color)
    lcd.message(message)
    sleep(1)
    while lcd.buttonPressed(lcd.SELECT) != 1:
        pass
    clean_display()


# Parse output
def parse(content):
    output = []
    if len(content) > 1:
        for line in content:
            if line != "":
                output.append(line[:-1])
        return output
    else:
            return content[0][:-1]


# Shell STDOUT
def run_command(bash):
    stdout = subprocess.Popen(bash.split(), stdout=subprocess.PIPE).stdout.readlines()
    return parse(stdout)


# Readfile
def readfile(file):
    f = open(file, 'ro')
    content = f.readlines()
    f.close()
    return parse(content)


# Color Matrix
def set_color(c):
    colors = {"YELLOW": lcd.YELLOW,
              "GREEN": lcd.GREEN,
              "TEAL": lcd.TEAL,
              "BLUE": lcd.BLUE,
              "VIOLET": lcd.VIOLET,
              "RED": lcd.RED,
              "OFF": lcd.OFF,
              "ON": lcd.ON}
    lcd.backlight(colors[c])
COLORS = ("YELLOW", "GREEN", "TEAL", "BLUE", "VIOLET", "RED")


# Random Background Color
def random_bg_color():
    n = randint(0, 5)
    set_color(COLORS[n])


# Menu
def menu_control():
    i = 0           # set index to 0
    menu_pos = []   # init Tracker

    while True:
        menu_id = menu_list
        # sub-menu handling
        if len(menu_pos) > 0:
            # load sub-menu path
            for m in menu_pos:
                menu_id = menu_id[m]
            menu_id = menu_id[1]
            # add back option
            if not ("\n< Back", "<back") in menu_id:
                menu_id.append(("\n< Back", "<back"))

        menu_text = menu_id[i][0]
        menu_item = menu_id[i][1]

        lcd.clear()
        lcd.backlight(lcd.TEAL)
        lcd.message(menu_text)
        # add + for sub-menu (FIXME only print + w/o spaces)
        if not type(menu_item) is str:
            lcd.message("\n               +")

        stime = 0       # reset screensaver timer

        # Controls
        while True:
            sleep(0.25)

            # Move Down
            if lcd.buttonPressed(lcd.DOWN):
                if i >= len(menu_id) - 1:
                    i = 0
                    sleep(0.2)  # extra wait on end
                else:
                    i += 1
                    sleep(0.1)
                break

            # Move Up
            if lcd.buttonPressed(lcd.UP):
                if i <= 0:
                    i = len(menu_id) - 1
                    sleep(0.2)  # extra wait on end
                else:
                    i -= 1
                    sleep(0.1)
                break

            # Select item
            if lcd.buttonPressed(lcd.SELECT):
                lcd.backlight(lcd.BLUE)
                sleep(0.1)
                # check for command or sub-menu
                if type(menu_item) is str:
                    if menu_item != "<back":
                        clean_display()
                        # execute command
                        exec menu_item
                    else:  # leave sub-menu
                        i = menu_pos[-1]    # set sub-menu parent
                        del menu_id[-1]     # remove back button from list
                        del menu_pos[-1]        # tuple
                        if len(menu_pos) > 0:
                            del menu_pos[-1]    # list
                else:  # join sub-menu
                    if len(menu_pos) > 0:
                        menu_pos.append(1)      # list
                    menu_pos.append(i)          # tuple
                    i = 0
                break

            # Screensaver
            stime += 1
            if stime >= 480:    # 480 * sleep(0.25) = 2m
                show_clock()
                break

############
# START
############
startup()
menu_control()
