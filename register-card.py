#!/usr/bin/python

import sys
import time 
import serial
import RPi.GPIO as GPIO
from sql import SqlAccess, NoMemberException, NoEventException, NoUnregisteredCardException
from io_cli import CLI
import ConfigParser

# Input/Output
io = CLI()

io.log("Using event name from config file...")	
cfg = ConfigParser.ConfigParser()
cfg.readfp(open(r'db/slugscan.cfg'))
eventName = cfg.get('Session', 'event').lower()

# Init SQL
sql = SqlAccess(eventName, io)


def cleanName(name):
	new = str(name)
	new = new.lower().capitalize()
	return new

def createMember(unregId):
	# Create member prompt, if enable new user flag is set
	# Get user input
	card = sql.getUnregCard(unregId)
	cardNum = card['cardNum']
	try:
		name = io.getName()	
		sql.createMember(cardNum,cleanName(name['fst']),cleanName(name['lst']))
	
	except Exception as e:
		io.error(e)
		io.error("Creating member failed.")
		return
	
	io.output("Removing card " + cardNum + " from unregistered card list (ID: " + str(unregId) + ")" )
	sql.removeUnregCard(unregId)
	io.output("Successfully created new member, please rescan card to sign in.")


try:
	cardList = sql.getUnregCards()
	io.listUnregisteredCards(cardList)
except NoUnregisteredCardException: 
	io.log("No unregistered cards listed, exiting...")
	sys.exit(0)
unregId = io.getUnregCardId()
createMember(unregId)
