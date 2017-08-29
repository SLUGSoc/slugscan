#!/usr/bin/python

import ConfigParser
import os
from sql_driver import SqlDriver

class NoMemberException(Exception):
	pass

class NoEventException(Exception):
	pass

class NoRegisterException(Exception):
	pass

class SqlException(Exception):
	pass

class SqlAccess:	
	def getEventId(self, eventName):
		# get event id, by finding event of same name
		res = self.db.queryGetSingle("SELECT * FROM events WHERE name=?", (eventName,))
		if (res is None):
			raise NoEventException("No event exists in database!")
		else:
			return res[0]

	def createEvent(self, eventName):
		self.db.queryWrite("INSERT INTO events (name) VALUES (?)", (eventName,))

	def currentEventId(self):
		# get current event id, by finding event of same name, or by creating if non-existent
		try:
			eId = self.getEventId(self.eventName)
		except NoEventException:
			self.createEvent(self.eventName)
			eId = self.getEventId(self.eventName)	
		return eId

	def __init__(self, eventName, logger):
		self.log = logger
		self.eventName = eventName
		self.db = SqlDriver(self.log)
		self.eventId = self.currentEventId()
		self.log.out("Event Name: " + self.eventName)
		self.log.out("Event ID: " + str(self.eventId))

	def addMemberToEvent(self, memberDict, eventId):
		self.db.queryWrite("INSERT INTO register (memberId,eventId,isPresent) "
							 "VALUES (?,?,1)",(memberDict['id'], eventId))

	def updateRegisterMember(self, memberDict):
		try:
			# Change member's presence at event
			currentlyPresent = self.checkMemberIsPresent(memberDict, self.eventId)
			self.updatePresence(memberDict, self.eventId, currentlyPresent)

		except NoRegisterException as e:
			# Add member to register for event
			self.addMemberToEvent(memberDict, self.eventId)
			self.log.out(memberDict['name'] + " signed in @ " + self.eventName)

	def updatePresence(self, memberDict, eventId, currentlyPresent):
		statusStr = " signed in @ "
		newPresence = 1
		if(currentlyPresent):
			statusStr = " signed out @ "
			newPresence = 0

		self.db.queryWrite("UPDATE register SET isPresent=? WHERE "
							"memberId=? AND eventId=?",(newPresence, memberDict['id'], eventId))
		self.log.out(memberDict['name'] + statusStr + self.eventName)

	def checkMemberIsPresent(self, memberDict, eventId):
		res = self.db.queryGetSingle("SELECT * FROM register WHERE memberId=? AND eventId=?", 
										(memberDict['id'], eventId))
		if (res is None):
			raise NoRegisterException("Member not yet registered at event")
			return
		if (res[2] == 1):
			return True
		else:
			return False

	def getMemberForCard(self,cardNum):	
		res = self.db.queryGetSingle("SELECT * FROM members WHERE cardNum=?", (cardNum,))
		# return memberId, names as dictionary
		if (res is None):
			raise NoMemberException("No member exists in database!")
		else:
			memberDict = {
							'id': 		res[0],
							'name': 	str(res[2]) + " " + str(res[3]),
							'alias': 	res[4] 
							}
		return memberDict

	def createMember(self,cardNum,firstName,lastName,isPaidMember=True):
		# exception if unsuccessful
		hasPaid = 0
		if (isPaidMember):
			hasPaid = 1
			insValues = (cardNum,firstName,lastName,hasPaid)
			self.db.queryWrite("INSERT INTO members (cardNum, firstName, lastName, hasPaid) "
								"VALUES (?,?,?,?)", insValues)
