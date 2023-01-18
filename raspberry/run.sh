#!/bin/bash
sudo pigpiod
nohup python3 /home/pi/projet/camera.py &
python3 /home/pi/projet/main.py
