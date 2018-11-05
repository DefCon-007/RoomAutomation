#!/bin/sh
cd /home/pi/roomAutomation/
./start-ngrok.sh
nohup python roomAutomation.py &
sleep 10 
cd /home/pi/roomAutomation/
python /home/pi/roomAutomation/addressUpdater.py
