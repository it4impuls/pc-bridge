#!/bin/bash
git pull
pip install -r req.txt
python3 PC_bridge/manage.py makemigrations
python3 PC_bridge/manage.py migrate
python3 PC_bridge/manage.py runserver 0.0.0.0:8000
