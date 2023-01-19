#!/bin/bash
sudo pigpiod
nohup python3 camera.py &
python3 main.py
