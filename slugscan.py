#!/usr/bin/python

import time 
import serial
import argparse
from io_gui import GUI
from io_gpio import GPIOAccess
import ConfigParser
import requests
import random

# The location of the deployed version of slugscan.gs
# where SCRIPT_ID is the unique ID of the script
GSCRIPTLOCATION = "https://script.google.com/macros/s/SCRIPT_ID/exec"

# One of these messages will randomly be shown upon successful sign in
signins = [
"Welcome %s.",
"Ready to pwn, %s?",
"%s logged in.",
"Get fragging %s!",
"You're all set %s.",
"It's dangerous to go alone, %s.",
"It's been a long time %s, how have you been?",
"It's time to kick ass, %s.",
"Gotta go fast, %s.",
"Stay awhile, and listen, %s.",
"\"LAN. LAN. I'm at LAN. LAAAAAAANNNN!!\" - %s",
"LAN isn't about why! It's about why not, %s.",
"The price of LAN is eternal vigilance, %s.",
"When life gives you lemons, make LAN, %s.",
"Sleep well, %s?",
"Come on, %s - go, go, go!",
"Trust me, %s.",
"Wake me when you need me, %s.",
"Be wise. Be safe. Be at a LAN, %s."
]

# One of these messages will randomly be shown upon successful sign out
signouts = ["Goodbye %s.",
"End of line, %s.",
"%s has low health!",
"%s has died of dysentery.",
"Game over, %s.",
"Stop. Stop and smell the ashes, %s.",
"Too bad you're out of gum, %s.",
"LAN. LAN never changes, %s.",
"Killing you is hard. Don't come back %s.",
"Endure and survive %s.",
"\"I miss the LAN.\" - %s",
"No matter how dark, the LAN always comes, %s." # as long as it can get really,
"Stop right there %s.",
"\"Country roads, take me home...\" - %s",
"\"Send me out... with a bang.\" - %s",
"Even in dark times, %s" + ", LAN.",
"Requiescat in pace, %s.",
"Heroes never die, %s.",
"%s fainted."
]


# Input/Output
io = GUI()
gpio = GPIOAccess()

# Parse commandline arguments
argParser = argparse.ArgumentParser(description='RFID card register system')
argParser.add_argument('event', nargs='?', type=str, help='Name of the current event, uses event in db/slugscan.cfg if left empty')
argParser.add_argument('eventnum', nargs='?', type=int, help='Number of the current event, uses eventnum in db/slugscan.cfg if left empty')

args = argParser.parse_args()
eventName = args.event
eventNumber = args.eventnum

if (eventName is None):
	io.log("Using event name from config file...")	
	cfg = ConfigParser.ConfigParser()
	cfg.readfp(open(r'db/slugscan.cfg'))
	eventName = cfg.get('Session', 'event')
else:
	eventName = eventName[0]

if (eventNumber is None):
	io.log("Using event number from config file...")	
	cfg = ConfigParser.ConfigParser()
	cfg.readfp(open(r'db/slugscan.cfg'))
	eventNumber = cfg.get('Session', 'eventnum')
else:
	eventNumber = eventNumber[0]


# RDM6300 Flags
#RESCAN_DELAY = 1.3
RESCAN_DELAY = 3 # this is also the amount of time text is shown on the screen...
FLAG_START = '\x02';
FLAG_STOP =  '\x03';
RDM_READ_LENGTH = 14;

PortRF = serial.Serial('/dev/serial0',9600)


# Init
io.showEvent(eventName, eventNumber)


def processCard(cardNum):
	print("Processing Card: " + cardNum)
	gpio.successfulScan()
	try:
		# DO WEB STUFF
		r = requests.get(GSCRIPTLOCATION + "?card=" + cardNum)

		print("Status: %i" % r.status_code)

		if r.status_code != 200:
			io.log("Connection error...")
			io.showRegisterUpdate("Connection error, please try again/see a tech...")
			gpio.failedScan()
		else:
			r = r.text.strip()
			print(r)
			if r[:4] == "????":
				io.log("Unknown user")
				io.showRegisterUpdate("Unknown user, please try again/see a tech...")
				gpio.failedScan()
			else:
				username = r[:-1]
				inorout = r[-1:]
				print(inorout)
				if inorout == "1":
					n = random.randint(0, len(signins)-1)
					s = signins[n] % username + " (in)"
				else:
					n = random.randint(0, len(signouts)-1)
					s = signouts[n] % username + " (out)"
				io.log(s)
				io.showRegisterUpdate(s)
				gpio.successfulScan()
		
	except Exception as e:
		io.showRegisterUpdate("Unknown error, please try again/see a tech...")
		gpio.failedScan()
		io.log(e)

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

				digit1 = int(cId[2:4], 16)
				digit2 = int(cId[4:6], 16)
				digit3 = int(cId[6:8], 16)
				digit4 = int(cId[8:10], 16)

				cId2 = (digit1 << 24) + (digit2 << 16) + (digit3 << 8) + digit4
				cId2 = str(cId2)

				io.log("Read Card: " + cId2)
				processCard(cId2)
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
