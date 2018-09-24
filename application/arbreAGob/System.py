#!/usr/bin/python2.7

import csv

def getSystemDict( index="system.csv", dataPath="/home/pi/data/barbare/" ):

    systemDict = {}

    # load csv data
    dataIndex = csv.reader( open( dataPath + index ) , delimiter=';')
   
    for line in dataIndex:
        code = line[0]
        command = line[1]
        systemDict[code] = command

    print "System keys mapped"
    return systemDict


