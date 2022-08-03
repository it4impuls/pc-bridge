#!/usr/bin/env python3

import RPi.GPIO as GPIO
import time




def pressButton():
	print("starting")

	GPIO.setmode(GPIO.BCM)

	GPIO.setup (25, GPIO.OUT)
	GPIO.setup (23, GPIO.IN)

	GPIO.output(25, True)
	time.sleep(0.5)
	GPIO.output(25, False)
	time.sleep(1)
	GPIO.cleanup()


def startPc():
	if getStatus(23) is False:
		pressButton()


def shutdownPc():
	if getStatus(23):
		pressButton()


def getStatus(gpio=23):

	GPIO.setmode(GPIO.BCM)

	GPIO.setup (25, GPIO.OUT)
	GPIO.setup (23, GPIO.IN)
	status = GPIO.input(gpio)
	time.sleep(0.2)
	GPIO.cleanup()
	return status