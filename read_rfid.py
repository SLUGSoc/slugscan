#!/usr/bin/python

import time 
import serial
import RPi.GPIO as GPIO
from sql import SqlAccess, NoMemberException, NoEventException

# RDM6300 Flags
FLAG_START = '\x02';
FLAG_STOP =  '\x03';
RDM_READ_LENGTH = 14;

RESCAN_DELAY = 0.8

GPIO.setmode(GPIO.BOARD)

PortRF = serial.Serial('/dev/ttyAMA0',9600)

# Init SQL
# TODO : event name as parameter
sql = SqlAccess("test event")

def createMember(cardNum):
	# Create member prompt, if enable new user flag is set
	# Get user input
	print "No member entry present, creating new member..."
	try:
		# TODO : Input sanitisation
		fst = raw_input("Enter first name: ")	
		lst = raw_input("Enter last name: ")	
		sql.createMember(cardNum,str(fst),str(lst))
	except Exception as e:
		print e
		print "Creating member failed, please rescan card."
		return
	print "Successfully created new member, please rescan card to sign in."
	
def processCard(cardNum):
	print "Processing Card: " + cardNum
	try:
		member = sql.getMemberForCard(cardNum)
	except NoMemberException as e:
		print e
		createMember(cardNum)
		return

	time.sleep(RESCAN_DELAY)	

def readRDM6300():
	cId = ""
	PortRF.flushInput()
	PortRF.flushOutput()
	readByte = PortRF.read()
	if readByte == FLAG_START:
		for i in range(RDM_READ_LENGTH):
			readByte = PortRF.read()
			if readByte == FLAG_STOP:
				break
			cId = cId + str(readByte)
		# TODO : checksum?
		readByte = None
		print "Read Card: " + cId
		processCard(cId)

# Main control loop
while True:
	readRDM6300()
