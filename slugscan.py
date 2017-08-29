#!/usr/bin/python

import time 
import serial
import RPi.GPIO as GPIO
import argparse
from sql import SqlAccess, NoMemberException, NoEventException
from logger import Logger

# Parse commandline arguments
argParser = argparse.ArgumentParser(description='RFID card register system')
argParser.add_argument('event', nargs=1, type=str, help='Name of the current event')

args = argParser.parse_args()
eventName = args.event

if (eventName is None):
	print "An event name must be provided!"
	raise SystemExit

eventName = eventName[0].lower()

# RDM6300 Flags
FLAG_START = '\x02';
FLAG_STOP =  '\x03';
RDM_READ_LENGTH = 14;

RESCAN_DELAY = 0.8

GPIO.setmode(GPIO.BOARD)

PortRF = serial.Serial('/dev/ttyAMA0',9600)

# Output
log = Logger()

# Init SQL
sql = SqlAccess(eventName, log)

def cleanName(name):
	new = str(name)
	new = new.lower().capitalize()
	return new

def createMember(cardNum):
	# Create member prompt, if enable new user flag is set
	# Get user input
	log.out("No member entry present, creating new member...")
	try:
		fst = raw_input("Enter first name: ")	
		lst = raw_input("Enter last name: ")	
		sql.createMember(cardNum,cleanName(fst),cleanName(lst))

	except Exception as e:
		log.error(e)
		log.error("Creating member failed, please rescan card.")
		return

	print "Successfully created new member, please rescan card to sign in."

def processCard(cardNum):
	print "Processing Card: " + cardNum
	try:
		member = sql.getMemberForCard(cardNum)
		log.out(member)
		sql.updateRegisterMember(member)
	except NoMemberException as e:
		log.out(e)
		createMember(cardNum)

	time.sleep(RESCAN_DELAY)	

def readRDM6300():
	cId = ""
	PortRF.flushInput()
	PortRF.flushOutput()
	readByte = PortRF.read()
	if readByte == FLAG_START:
		for i in range(RDM_READ_LENGTH + 1):
			readByte = PortRF.read()
			if readByte == FLAG_STOP:
				# Card finished reading, process it
				readByte = None
				log.out("Read Card: " + cId)
				processCard(cId)
				return
		
			elif (i > RDM_READ_LENGTH):
				# Exceeded possible card length
				log.error("Invalid card read, please rescan the card.")
				return

			cId = cId + str(readByte)
	
# Main control loop
while True:
	readRDM6300()
