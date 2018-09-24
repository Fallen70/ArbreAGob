#!/usr/bin/python2.7

import sys
from SoundLoader import *
from KeyboardLoader import *
from System import *
from Digicode import mainLoop as digicode 
from Jukebox import mainLoop as jukebox 
from Memory import mainLoop as memory 
from Sequence import *


ACTIVITE = { 'digicode' : digicode,
             'jukebox'  : jukebox,
             'memory'  : memory,
           }


def main( deviceName="Dell", datadir="barebare" ):

    systemSound = getSoundDict( dataPath="/home/pi/data/system/" )
    # load csv data
    switch = csv.reader( open("/home/pi/data/system/switch.csv") , delimiter=';')
    switchDict = {}

    for line in switch:
        code = line[0]
        dirName = line[1]
        activite = line[2]
        switchDict[code] = { 'dir' : dirName, 'activite' : ACTIVITE[activite] } 

    keys = switchDict.keys() 
    device = getDeviceObject( deviceName )

    systemDict = getSystemDict( dataPath= "/home/pi/data/system/" )

    print "Choix du dossier de son"
    # Wait for good input
    playSound( systemSound, 'demarrage', True ) 
    selection = {}
    while True:
        event = device.read_one()
        if None <> event and event.type == evdev.ecodes.EV_KEY and event.value == 1:
            c = "%d" %(event.code)
            if c in keys:
                selection = switchDict[c]
                playSound( systemSound, 'ready', True ) 
                break
            else:
                playSound( systemSound, 'error', True )


    print "Chargement des sequences"

    # load sequence data
    seqdata = csv.reader( open("/home/pi/data/" + selection['dir'] + "/sequence.csv") , delimiter=';')
    seqDict = {}

    for line in seqdata:
        code = line[0]
        seqTxt = line[1]
        print code,seqTxt
        seqDict[code] = Sequence( seqTxt )

    selection['activite']( deviceName=deviceName , datadir=selection['dir'], systemSound=systemSound, seqDict=seqDict, systemDict=systemDict )


if __name__ == '__main__' :
    if len ( sys.argv ) > 1  :
        keyboardName = sys.argv[1]
        main( deviceName=keyboardName )    
    else :
        mainLoop()
