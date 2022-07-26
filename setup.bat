@ECHO OFF
if exist %~dp0env\ (
    GOTO runner
) else (
    GOTO installer
)


:installer
ECHO instaling enviroment...
START /B /WAIT py -m venv %~dp0env
GOTO runner
:end

:runner
ECHO starting programm...
ECHO installing libraries...
START /B /WAIT %~dp0env\Scripts\python.exe -m pip install -r %~dp0req.txt
START /B /WAIT %~dp0env\Scripts\python.exe PC_bridge\manage.py makemigrations
START /B /WAIT %~dp0env\Scripts\python.exe PC_bridge\manage.py migrate
START /B /WAIT %~dp0env\Scripts\python.exe PC_bridge\manage.py runserver
GOTO end

:end
echo done
