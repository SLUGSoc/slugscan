import time 
import serial
import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BOARD)

PortRF = serial.Serial('/dev/ttyAMA0',9600)

while True:
	id = ""
	readByte = PortRF.read()
	if readByte == "\x02":
		for i in range(12):
			readByte = PortRF.read()
			id = id + str(readByte)
		print id
