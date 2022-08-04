#!/usr/bin/env python3

from sys import platform

if platform == "linux" or platform == "linux2":
	import RPi.GPIO as GPIO
import time
import sqlite3
from os import path




def pressButton(power_gpio):
	if not 0<power_gpio<41 and not platform == "linux" or platform == "linux2":
		return
	print("pressing button")
	GPIO.setmode(GPIO.BCM)
	GPIO.setup (power_gpio, GPIO.OUT)

	GPIO.output(power_gpio, True)
	time.sleep(0.2)
	GPIO.output(power_gpio, False)
	time.sleep(0.5)
	GPIO.cleanup()


def startPc(status_gpio:int, power_gpio:int):
	if not 0<status_gpio<41 and not 0<power_gpio<41 and not platform == "linux" or platform == "linux2":
		return
	if not getStatus(status_gpio):
		pressButton(power_gpio)
	else:
		print("already online")

def shutdownPc(status_gpio:int, power_gpio:int):
	if not 0<status_gpio<41 and not 0<power_gpio<41 and not platform == "linux" or platform == "linux2":
		return
	if getStatus(status_gpio):
		pressButton(power_gpio)
	else:
		print("already offline")


def getStatus(status_gpio:int):
	if not 0<status_gpio<41 and not platform == "linux" or platform == "linux2":
		return 3
	GPIO.setmode(GPIO.BCM)
	GPIO.setup (status_gpio, GPIO.IN)

	status = GPIO.input(status_gpio)
	time.sleep(0.1)
	GPIO.cleanup()

	updateStatus(status_gpio, status)
	return status

def waitForChange(desiredStatus:int, status_gpio:int):
	starttime = time.time()
	currtime = time.time()
	while currtime - starttime < 10:
		if getStatus(status_gpio) == desiredStatus:
			return True
		time.sleep(0.2)
		currtime = time.time()
	print("timeout after ", currtime - starttime)
	return False

def readUpdateAll():
	p = path.join(path.split(path.dirname(path.abspath(__file__)))[0], "db.sqlite3")
	con = sqlite3.connect(p)
	cur = con.cursor()
	data = cur.execute('''SELECT id, pcie_status, status FROM PCManager_pc''')
	for i in data.fetchall():  
		pk = i[0]  
		pcie_status = i[1]
		status_old = i[2]
		if platform == "linux" or platform == "linux2":
			status = getStatus(pcie_status)
		else:
			status = 0 
		if status != status_old:
			cur.execute('''UPDATE PCManager_pc SET status=? WHERE id=?''', (status, pk))

	cur.close()    
	con.commit()

def updateStatus(status_gpio:int, status:int):
	p = path.join(path.split(path.dirname(path.abspath(__file__)))[0], "db.sqlite3")
	con = sqlite3.connect(p)
	cur = con.cursor()
	# cur.execute('''SELECT * FROM PCManager_pc''')
	# print("updating gpio ", status_gpio, " to", status)
	cur.execute('''UPDATE PCManager_pc SET status=? WHERE pcie_status=?''', (status, status_gpio))
	cur.close()    
	con.commit()

def main():
	readUpdateAll()
	


if __name__ == '__main__':
    main()