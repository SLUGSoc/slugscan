#!/usr/bin/python

import time 
import serial
import RPi.GPIO as GPIO
import argparse
from sql import SqlAccess, NoMemberException, NoEventException
from io_cli import CLI

GPIO.setmode(GPIO.BOARD)

# Parse commandline arguments
argParser = argparse.ArgumentParser(description='RFID card register system')
argParser.add_argument('event', nargs=1, type=str, help='Name of the current event')

args = argParser.parse_args()
eventName = args.event

if (eventName is None):
	print "An event name must be provided!"
	raise SystemExit
else:
	eventName = eventName[0].lower()


# RDM6300 Flags
RESCAN_DELAY = 0.8
FLAG_START = '\x02';
FLAG_STOP =  '\x03';
RDM_READ_LENGTH = 14;

PortRF = serial.Serial('/dev/serial0',9600)


# Input/Output
io = CLI()

# Init SQL
sql = SqlAccess(eventName, io)


def cleanName(name):
	new = str(name)
	new = new.lower().capitalize()
	return new

def createMember(cardNum):
	# Create member prompt, if enable new user flag is set
	# Get user input
	io.output("No member entry present, creating new member...")
	try:
		name = io.getName()	
		sql.createMember(cardNum,cleanName(name['fst']),cleanName(name['lst']))

	except Exception as e:
		io.error(e)
		io.error("Creating member failed, please rescan card.")
		return

	print "Successfully created new member, please rescan card to sign in."

def processCard(cardNum):
	print "Processing Card: " + cardNum
	try:
		member = sql.getMemberForCard(cardNum)
		io.output(member)
		sql.updateRegisterMember(member)
	except NoMemberException as e:
		io.output(e)
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
				io.output("Read Card: " + cId)
				processCard(cId)
				return
		
			elif (i > RDM_READ_LENGTH):
				# Exceeded possible card length
				io.error("Invalid card read, please rescan the card.")
				return

			cId = cId + str(readByte)
	
# Main control loop
while True:
	readRDM6300()
