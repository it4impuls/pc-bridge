#!/usr/bin/env python3

import RPi.GPIO as GPIO
import time




def pressButton(power_gpio = 25):
	GPIO.setmode(GPIO.BCM)
	GPIO.setup (power_gpio, GPIO.OUT)

	GPIO.output(power_gpio, True)
	time.sleep(0.2)
	GPIO.output(power_gpio, False)
	time.sleep(0.5)
	GPIO.cleanup()


def startPc(status_gpio = 23, power_gpio = 25):
	if getStatus(23) is False:
		pressButton()


def shutdownPc(status_gpio = 23, power_gpio = 25):
	if getStatus(23):
		pressButton()


def getStatus(status_gpio = 23):

	GPIO.setmode(GPIO.BCM)
	GPIO.setup (23, GPIO.IN)
	status = GPIO.input(status_gpio)
	time.sleep(0.1)
	GPIO.cleanup()
	return status