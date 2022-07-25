#!/bin/bash
[!-d "./venv/" ] && py -m venv ./venv && ./venv/Scripts/python.exe -m pip install -r -/req.txt
./venv/Scripts/python.exe PC_bridge/manage.py runserver

# installer()
# {
#     echo "instaling enviroment..."
#     py -m venv ./venv
#     echo "installing libraries..."
#     ./venv/Scripts/python.exe -m pip install -r -/req.txt
#     runner
# }

# runner()
# {
#     echo "starting programm..."
#     ./venv/Scripts/python.exe PC_bridge/manage.py runserver
# }
echo "done"
