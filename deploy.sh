#!/bin/sh
cd /home/pi/roomAutomation/
./start-ngrok.sh
nohup gunicorn roomAutomation:app -b 127.0.0.1:1234 &
sleep 10 
cd /home/pi/roomAutomation/
python /home/pi/roomAutomation/addressUpdater.py
