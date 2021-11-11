#!/bin/bash
#This script is used to execute the program

path=$(pwd)

gnome-terminal -x bash -c "cd ${path} && source venv/bin/activate && pip install -r requirements.txt && python3 server.py"
sleep 1
gnome-terminal -x bash -c "cd ${path} && source venv/bin/activate && pip install -r requirements.txt && python3 viewer.py"
sleep 1
gnome-terminal -x bash -c "cd ${path} && source venv/bin/activate && pip install -r requirements.txt && python3 client.py"