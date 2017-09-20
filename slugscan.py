#!/usr/bin/python

import time 
import serial
import RPi.GPIO as GPIO
import argparse
from sql import SqlAccess, NoMemberException, NoEventException
from io_cli import CLI
from io_gui import GUI, UserPermissionException
import ConfigParser

GPIO.setmode(GPIO.BOARD)

# Input/Output
# TODO argument to enable cli mode
io = GUI()

# Parse commandline arguments
argParser = argparse.ArgumentParser(description='RFID card register system')
argParser.add_argument('event', nargs='?', type=str, help='Name of the current event, uses event in db/slugscan.cfg if left empty')

args = argParser.parse_args()
eventName = args.event

if (eventName is None):
	io.log("Using event name from config file...")	
	cfg = ConfigParser.ConfigParser()
	cfg.readfp(open(r'db/slugscan.cfg'))
	eventName = cfg.get('Session', 'event').lower()
else:
	eventName = eventName[0].lower()


# RDM6300 Flags
RESCAN_DELAY = 0.8
FLAG_START = '\x02';
FLAG_STOP =  '\x03';
RDM_READ_LENGTH = 14;

PortRF = serial.Serial('/dev/serial0',9600)


# Init SQL
sql = SqlAccess(eventName, io)


def cleanName(name):
	new = str(name)
	new = new.lower().capitalize()
	return new

def createMember(cardNum):
	# Create member prompt, if enable new user flag is set
	# Get user input
	io.log("No member entry present, creating new member...")
	try:
		name = io.getName()	
		sql.createMember(cardNum,cleanName(name['fst']),cleanName(name['lst']))
	
	except UserPermissionException:
		io.output("Card not yet registered, inform a committee member. [" + str(cardNum) + "]")
		time.sleep(2)
		return

	except Exception as e:
		io.error(e)
		io.error("Creating member failed, please rescan card.")
		return

	print "Successfully created new member, please rescan card to sign in."

def processCard(cardNum):
	print "Processing Card: " + cardNum
	try:
		member = sql.getMemberForCard(cardNum)
		io.log(member)
		sql.updateRegisterMember(member)

	except NoMemberException as e:
		io.log(e)
		createMember(cardNum)

	time.sleep(RESCAN_DELAY)
	io.output("Please scan card...")

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
				io.log("Read Card: " + cId)
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
	io.update()
