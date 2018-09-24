#!/usr/bin/python2.7

import sys
from KeyboardLoader import *

# devices = [evdev.InputDevice(fn) for fn in evdev.list_devices()]
# for device in devices:
#   print(device.fn, device.name, device.phys)

# device = evdev.InputDevice('/dev/input/event1')
# print(device)
# device /dev/input/event1, name "USB Keyboard", phys "usb-0000:00:12.1-2/input0"
# 
# for event in device.read_loop():
#     if event.type == evdev.ecodes.EV_KEY:
#         print(categorize(event))
#         # pressing 'a' and holding 'space'



def mainLoop( deviceName = "Keyboard" , sequence = [ '16','17','18', '19' ]):
    device = getDeviceObject( deviceName )
    while True:
       event = device.read_one()
       if None <> event and event.type == evdev.ecodes.EV_KEY and event.value == 1:
           c = "%d" %(event.code)
           print "CODE : %s" %c
           print event


if __name__ == '__main__' :
    if len ( sys.argv ) > 1  :
        keyboardName = sys.argv[1]
        mainLoop( deviceName=keyboardName )    
    else :
        mainLoop()
