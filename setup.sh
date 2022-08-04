#!/bin/bash
pip install -r req.txt
python3 PC_bridge/manage.py makemigrations
python3 PC_bridge/manage.py migrate
sudo python3 PC_bridge/manage.py runserver 0.0.0.0:8000
