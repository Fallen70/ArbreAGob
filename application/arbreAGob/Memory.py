#!/usr/bin/python2.7

import sys
import random
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


def resetOrdre( soundDict ):
    keyToConsume = list( soundDict.keys() )
    while keyToConsume:
        kSwitch1 = random.choice( keyToConsume )
        temp1 = soundDict[kSwitch1]
        keyToConsume.remove(kSwitch1)
        kSwitch2 = keyToConsume.pop()
        temp2 = soundDict[kSwitch2]
        soundDict[kSwitch1] = temp2
        soundDict[kSwitch2] = temp1
    return soundDict

def mainLoop( deviceName = "Keyboard" , datadir="barbare" , systemSound=None, seqDict={}, systemDict={} ):
    soundDict = getSoundDict( dataPath= "/home/pi/data/" + datadir + "/" ) 
    device = getDeviceObject( deviceName )
    k = soundDict.keys() 
    kSystem = systemDict.keys() 
    if systemSound:
        print "READY"
        print datadir
        playSound( systemSound, 'ready', True ) 
    stop = False
    while not stop:
        reset = False
        played = []
        listSeqIdFound = []
        foundCount = 0
        soundDict = resetOrdre( soundDict )     
        while not reset:
            if len( listSeqIdFound ) == len( seqDict.keys() ):
                playSound( soundDict, 'grande_victoire', True)
                reset = True
                continue
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
                    if seqId in listSeqIdFound :
                        playSound( soundDict, 'deja_trouve', True)
                        continue
                    seqDict[seqId].addCode( c )
                    print "Sequence : ", seqDict[seqId].seq
                    print "Current : ", seqDict[seqId].current 
                    if seqId in played:
                        foundCount += 1
                        playSound( soundDict, "win%d" %foundCount, True )
                        listSeqIdFound.append( seqId )
                        played = []
                        continue
                    elif not played :
                        played.append( seqId )
                        playSound( soundDict, c, True, jukebox=seqDict[seqId].jukebox )
                    else:
                        played = []
                        playSound( soundDict, 'erreur', True)
                        continue
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
