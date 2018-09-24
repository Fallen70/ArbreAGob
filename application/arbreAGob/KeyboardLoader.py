
#!/usr/bin/python2.7

import evdev 

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

def getInputDeviceName( keyboardName ):
    results=[]
    for device in [evdev.InputDevice(fn) for fn in evdev.list_devices()]:
        if keyboardName in device.name:
            results.append( device.fn )
    results.sort()
    print keyboardName + " on " + results[0]
    return results[0]

def getDeviceObject( keyboardName ):
    inputName = getInputDeviceName( keyboardName )
    device = evdev.InputDevice( inputName )
    print device
    return device
