@ECHO OFF
IF EXIST venv\ GOTO runner
ELSE GOTO installer


:installer
ECHO instaling enviroment...
START /B /WAIT py -m venv %~dp0venv
ECHO installing libraries...
START /B /WAIT %~dp0venv\Scripts\python.exe -m pip install -r %~dp0req.txt
GOTO runner

:runner
ECHO starting programm...
start "" http://127.0.0.1:8000/pcmanager/
START /B /WAIT %~dp0venv\Scripts\python.exe PC_bridge\manage.py runserver
GOTO end

:end
echo done
