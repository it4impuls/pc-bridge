# PC-Bridge

Ein Programm, welches es ermöglicht den Status der Server-PC's einzusehen und diese remote starten zu können.


### Vorraussetzungen:
* Python3

starte setup.bat um eine lokale python enviroment zu erstellen und die nötigen libraries herunterzuladen.

Um den Server zu starten, führe start server aus. (die Website öffnet sicht bevor der Server hochgefahren ist. Einfach ein paar Sekunden warten und die Seite neu laden)



### default login:
Vor Inbetriebnahme ändern!!
Username: admin
Password: admin

### TODO:
* ~~Ermöglichen PC's in eine Datenbank Hinzuzufügen, Editieren, Löschen~~
* Mit PC's kommunizieren
* Status ermitteln und anzeigen
* Mit CSS verschönern


### Raspi info:
IP: 192.168.100.119

Vor Inbetriebnahme ändern!!
username: pcbridge
password: pcbridge01


### API
check status: GET request to WEBSITE/pcmanager/getstatus with params id=1
restart: POST request to WEBSITE/pcmanager/restart with body(formdata) id: 1
shutdown: POST request to WEBSITE/pcmanager/shutdown with body(formdata) id: 1