#!/bin/bash
pkill java
cd ..
xvfb-run java -Dwebdriver.chrome.driver=/usr/bin/chromedriver -jar selenium-server-standalone.jar &
cd RandomFun
python3 bot.py
