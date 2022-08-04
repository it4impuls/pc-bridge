#!/usr/bin/env python3

import RPi.GPIO as GPIO
import time




def pressButton(power_gpio = 25):
	print("pressing button")
	GPIO.setmode(GPIO.BCM)
	GPIO.setup (power_gpio, GPIO.OUT)

	GPIO.output(power_gpio, True)
	time.sleep(0.2)
	GPIO.output(power_gpio, False)
	time.sleep(0.5)
	GPIO.cleanup()


def startPc(status_gpio = 23, power_gpio = 25):
	if not getStatus(status_gpio):
		pressButton(power_gpio)
	else:
		print("already online")

def shutdownPc(status_gpio = 23, power_gpio = 25):
	if getStatus(23):
		pressButton(power_gpio)
	else:
		print("already offline")


def getStatus(status_gpio = 23):
	
	GPIO.setmode(GPIO.BCM)
	GPIO.setup (23, GPIO.IN)
	status = GPIO.input(status_gpio)
	print(status)
	time.sleep(0.1)
	GPIO.cleanup()
	return status

def waitForChange(desiredStatus, status_gpio = 23):
	starttime = time.time()
	currtime = time.time()
	while currtime - starttime < 10:
		if getStatus(status_gpio) == desiredStatus:
			return True
		time.sleep(0.2)
		currtime = time.time()
	print("timeout after ", currtime - starttime)
	return False