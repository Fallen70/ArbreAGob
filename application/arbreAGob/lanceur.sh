#!/bin/bash

cd /home/pi/application/arbreAGob/
sleep 5 
t=$(ps aux | grep ActiviteLoader.py | wc -l)
if [ $t -eq 1 ];
    #then python ActiviteLoader.py "USB USB Keyboard" ;
    then python ActiviteLoader.py "Dell" ;
fi

