#!/bin/sh
cd /home/pi/RoomAutomation/
nohup python roomAutomation.py &
sleep 3
./start-tunnel.sh
#cd /home/pi/RoomAutomation/
#python /home/pi/RoomAutomation/addressUpdater.py
