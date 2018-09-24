#!/usr/bin/python2.7

import sys,time
from SoundLoader import *
from KeyboardLoader import *
from Sequence import *

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


def resetSeq( seqDict, keys=[] ):
    for key in keys:
        print "Reset seq : %s" %key
        seqDict[key].reset()


def mainLoop( deviceName = "Keyboard" , datadir="barbare" , systemSound=None, seqDict={}, systemDict={} ):
    soundDict = getSoundDict( dataPath= "/home/pi/data/" + datadir + "/" ) 
    device = getDeviceObject( deviceName )
    k = soundDict.keys() 
    kSystem = systemDict.keys() 
    lastSeq = []
    if systemSound:
        print "READY"
        print datadir
        playSound( systemSound, 'ready', True ) 
    stop = False
    while not stop:
        reset = False
        resetSeq( seqDict, seqDict.keys() )
        while not reset:
            event = device.read_one()
            if None <> event and event.type == evdev.ecodes.EV_KEY and event.value == 1:
                c = "%d" %(event.code)
                v = "%d" %(event.value)
                print "Code : %s, value : %s" %( c, v )
                if c in kSystem:
                    if "RESET" == systemDict[c] :
                       reset = True
                       print "RESET" 
                       continue
                    if "SHUTDOWN" == systemDict[c] :
                       stop = True 
                       reset  = True
                       print "SHUTDOWN" 
                       break
                if c in k:
                    seqId = soundDict[c]['seq']
                    if seqId not in lastSeq:
                        resetSeq( seqDict, lastSeq )
                        lastSeq = [seqId]
                    seqDict[seqId].addCode( c )
                    print "Sequence : ", seqDict[seqId].seq
                    print "Current : ", seqDict[seqId].current 
                    if seqDict[seqId].isValid( ):
                        print "Win"
                        playSound( soundDict, c, force=True, jukebox=seqDict[seqId].jukebox )
                        time.sleep( soundDict[c]['sound'].get_length() )
                        playSound( soundDict, seqDict[seqId].win  )
                        time.sleep( soundDict[seqDict[seqId].win]['sound'].get_length() )
                    else:
                        playSound( soundDict, c, True, jukebox=seqDict[seqId].jukebox )
                if c not  in k:
                    print "Not binded"
    print "DOIT STOPPER"


if __name__ == '__main__' :
    if len ( sys.argv ) > 2  :
        keyboardName = sys.argv[1]
        data = sys.argv[2]
        mainLoop( deviceName=keyboardName, datadir=data )    
    else :
        mainLoop()
