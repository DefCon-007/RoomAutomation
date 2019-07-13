#!/bin/sh
cd /home/pi/RoomAutomation/
./start-serveo.sh
nohup python roomAutomation.py &
sleep 10 
#cd /home/pi/RoomAutomation/
#python /home/pi/RoomAutomation/addressUpdater.py
