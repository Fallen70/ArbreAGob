#!/usr/bin/python2.7

import csv,pygame,time

# load sound
# pygame.mixer.init()
# son = pygame.mixer.Sound("Clean_tapping_sample.ogg")

def getSoundDict( index="index.csv", dataPath="/home/pi/data/barbare/", chanels=32 ):

    soundDict = {}

    # load csv data
    dataIndex = csv.reader( open( dataPath + index ) , delimiter=';')
   
    if not pygame.mixer.get_init():
        startMixer( chanels )

    print "Mixer status : channels %d " %pygame.mixer.get_num_channels()

    for line in dataIndex:
        code = line[0]
        fileName = line[1]
        if len( line ) == 3 :
            seq = line[2]
        else :
            seq = None 
        sound = {}
        sound['name'] = fileName
        sound['sound'] = pygame.mixer.Sound( dataPath + fileName )
        sound['seq'] = seq
        soundDict[code] = sound

    print "Sound library loaded"
    return soundDict


def playSound( soundDict, code, force=False, jukebox=True ):
    s = soundDict[code]
    if jukebox:
        pygame.mixer.stop()
    chanel = pygame.mixer.find_channel(force)
    if None <> chanel:
        print "playing %(name)s" %s
        #chanel.play(s['sound'])
        chanel.queue(s['sound'])
    else:
        print "Unable to find free chanel"

def startMixer( chanels ):
    pygame.mixer.init( )
    pygame.mixer.set_num_channels(chanels)

def stopMixer():
    pygame.mixer.stop()
    pygame.mixer.quit()
