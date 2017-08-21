import time 
import serial
import RPi.GPIO as GPIO
import ConfigParser
import os

# Import config 
config = ConfigParser.ConfigParser()
config.readfp(open(r'slugscan.cfg'))

sqlUser = config.get('MySQL', 'username')
sqlPass = config.get('MySQL', 'password')
sqlHost = config.get('MySQL', 'host')
sqlDb	= config.get('MySQL', 'db')

print sqlUser
print sqlPass
print sqlHost
print sqlDb

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
