#!/bin/sh
cd /home/pi/RoomAutomation/
./start-ngrok.sh
nohup python roomAutomation.py &
sleep 10 
cd /home/pi/RoomAutomation/
python /home/pi/RoomAutomation/addressUpdater.py
