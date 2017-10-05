#!/usr/bin/python

import ConfigParser
import os
import datetime as DT
from sql_driver import SqlDriver

class NoMemberException(Exception):
	pass

class NoEventException(Exception):
	pass

class NoRegisterException(Exception):
	pass

class SqlException(Exception):
	pass

class NoUnregisteredCardException(Exception):
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

	def __init__(self, eventName, io):
		self.io = io
		self.eventName = eventName
		self.db = SqlDriver(self.io)
		self.eventId = self.currentEventId()
		self.io.showEvent(self.eventName, self.eventId)

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
			self.io.showRegisterUpdate(memberDict['name'] + " signed in @ " + self.eventName)

	def updatePresence(self, memberDict, eventId, currentlyPresent):
		statusStr = " signed in @ "
		newPresence = 1
		if(currentlyPresent):
			statusStr = " signed out @ "
			newPresence = 0

		self.db.queryWrite("UPDATE register SET isPresent=? WHERE "
							"memberId=? AND eventId=?",(newPresence, memberDict['id'], eventId))
		self.io.showRegisterUpdate(memberDict['name'] + statusStr + self.eventName)

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

	def createUnregCard(self, cardNum):
		time = DT.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
		insValues = (cardNum, time)
		self.db.queryWrite("INSERT INTO unregistered_cards (cardNum, time) "
							"VALUES (?, ?)", insValues)
	
	def updateUnregCard(self, unregId):	
		time = DT.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
		updValues = (time, unregId)
		self.db.queryWrite("UPDATE unregistered_cards SET time=? WHERE id=?", updValues)

	def removeUnregCard(self, unregId):
		# Remove card from unregistered table. Useful for when a card is registered.
		self.db.queryWrite("DELETE FROM unregistered_cards WHERE id=?", (unregId,))

	def getUnregCard(self, unregId):
		res = self.db.queryGetSingle("SELECT * FROM unregistered_cards WHERE id=?", (unregId,))
		if (res is None):
			raise NoUnregisteredCardException("Card not (yet) set as unregistered.")
		else:
			unregDict = {
							'id' :		res[0],
							'cardNum' : res[1],
							'time' :	res[2] 	
			}
			return unregDict

	def getUnregCardByNum(self, cardNum):
		res = self.db.queryGetSingle("SELECT * FROM unregistered_cards WHERE cardNum=?", (cardNum,))
		if (res is None):
			raise NoUnregisteredCardException("Card not (yet) set as unregistered.")
		else:
			unregDict = {
							'id' :		res[0],
							'cardNum' : res[1],
							'time' :	res[2] 	
			}
			return unregDict
	
	def getUnregCards(self):
		# Get list of unregistered card dicts
		res = self.db.queryGetMultiple("SELECT * FROM unregistered_cards", None)
		if not res:
			raise NoUnregisteredCardException("No unregistered cards scanned - scan one.")
		else:
			cardList = []
			for row in res:
				card = {
								'id' :		row[0],
								'cardNum' : row[1],
								'time' :	row[2] 	
				}
				cardList.append(card)
			return cardList
				
				
