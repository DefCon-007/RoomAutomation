#!/bin/sh
cd /home/pi/defcon-007.github.io/
git fetch origin master
git rebase origin/master
git add .
git commit -m "Updated room URL "
git push origin master