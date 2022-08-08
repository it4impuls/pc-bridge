#!/usr/bin/env python3

from sys import platform

if platform == "linux" or platform == "linux2":
	import RPi.GPIO as GPIO
import time
import sqlite3
from os import path


SAFE_GPIO = [5, 6, 12, 13, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27]

def pressButton(power_gpio:int):
	if validateGPIO(power=power_gpio):
		print("pressing button")
		GPIO.setmode(GPIO.BCM)
		GPIO.setup (power_gpio, GPIO.OUT)

		GPIO.output(power_gpio, True)
		time.sleep(0.1)
		GPIO.output(power_gpio, False)
		time.sleep(0.1)
		GPIO.cleanup()


def startPc(status_gpio:int, power_gpio:int):
	if validateGPIO(status=status_gpio, power=power_gpio):
		if not getStatus(status_gpio):
			pressButton(power_gpio)
		else:
			print("already online")

def shutdownPc(status_gpio:int, power_gpio:int):
	if validateGPIO(status=status_gpio, power=power_gpio):
		if getStatus(status_gpio):
			pressButton(power_gpio)
		else:
			print("already offline")


def getStatus(status_gpio:int):
	if validateGPIO(status=status_gpio):
		GPIO.setmode(GPIO.BCM)
		GPIO.setup (status_gpio, GPIO.IN)

		status = GPIO.input(status_gpio)

		time.sleep(0.1)
		GPIO.cleanup()
		updateStatus(status_gpio, status)
		return status
	else:
		print("invalid gpio")
		updateStatus(status_gpio, 3)
		return 3

def waitForChange(desiredStatus:int, status_gpio:int):
	starttime = time.time()
	currtime = time.time()
	while currtime - starttime < 10:
		if getStatus(status_gpio) == desiredStatus:
			return True
		time.sleep(0.1)
		currtime = time.time()
	print("timeout after ", currtime - starttime)
	return False

def readUpdateAll():
	p = path.join(path.split(path.dirname(path.abspath(__file__)))[0], "db.sqlite3")
	con = sqlite3.connect(p)
	cur = con.cursor()
	data = cur.execute('SELECT id, pcie_status, status FROM PCManager_pc')
	for i in data.fetchall():  
		pk = i[0]  
		pcie_status = i[1]
		status_old = i[2]
		if platform == "linux" or platform == "linux2":
			status = getStatus(pcie_status)
		else:
			status = 0 
		if status != status_old:
			cur.execute('UPDATE PCManager_pc SET status=? WHERE id=?', (status, pk))
	cur.close()    
	con.commit()

def updateStatus(status_gpio:int, status:int):
	p = path.join(path.split(path.dirname(path.abspath(__file__)))[0], "db.sqlite3")
	con = sqlite3.connect(p)
	cur = con.cursor()
	# cur.execute('''SELECT * FROM PCManager_pc''')
	# print("updating gpio ", status_gpio, " to", status)
	cur.execute('UPDATE PCManager_pc SET status=? WHERE pcie_status=?', (status, status_gpio))
	cur.close()    
	con.commit()

def validateGPIO(status:int=5, power:int=5):
	if status in SAFE_GPIO and power in SAFE_GPIO and platform == "linux" or platform == "linux2" and status != power:
		return True
	else:
		return False

def main():
	readUpdateAll()
	


if __name__ == '__main__':
    main()