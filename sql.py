#!/usr/bin/python

import ConfigParser
import os
import sqlite3

class NoMemberException(Exception):
	pass

class NoEventException(Exception):
	pass

class SqlException(Exception):
	pass

class SqlAccess:	
	def setupTables(self):
		self.curs.execute("CREATE TABLE IF NOT EXISTS members ("
					"id 		INTEGER		PRIMARY KEY, " 
					"cardNum 	CHARACTER(20)	UNIQUE NOT NULL, "
					"firstName 	NVARCHAR(32)	NOT NULL, "
					"lastName 	NVARCHAR(32)	NOT NULL, "
					"alias		NVARCHAR(32)	, "
					"hasPaid 	BOOLEAN		DEFAULT 1"
					")")
		self.curs.execute("CREATE TABLE IF NOT EXISTS events ("
					"id		INTEGER		PRIMARY KEY, "
					"name		NVARCHAR(32)	UNIQUE NOT NULL "
					")")
		self.curs.execute("CREATE TABLE IF NOT EXISTS register ("
					"memberId	INTEGER, "
					"eventId	INTEGER, "
					"isPresent	BOOLEAN		DEFAULT 0, "
					"FOREIGN KEY(memberId) 	REFERENCES members(id), "
					"FOREIGN KEY(eventId) 	REFERENCES events(id) "
					")")
	
	def getEventId(self, eventName):
		# get event id, by finding event of same name
		self.curs.execute("SELECT * FROM events WHERE name=?", (eventName))
		res = self.curs.fetchone()
		if (res is None):
			raise NoEventException("No event exists in database!")
		else:
			return res[0]

	def createEvent(self, eventName):
		self.curs.execute("INSERT INTO events (name) VALUES (?)", (eventName))
		self.conn.commit()
			
	def currentEventId(self):
		# get current event id, by finding event of same name, or by creating if non-existent
		try:
			eId = self.getEventId(self.eventName)
		except NoEventException:
			self.createEvent(self.eventName)
			eId = self.getEventId(self.eventName)	
		return eId

	def __init__(self, eventName):
		self.conn = sqlite3.connect('db/slugscan.db')
		self.curs = self.conn.cursor()
		self.setupTables()
		self.eventName = eventName
		self.eventId = self.currentEventId()
		print self.eventId
		self.conn.commit()
	
	def cleanup(self):
		self.conn.close()

	def addMemberToEvent(self,memberDict,eventId):
		self.curs.execute("INSERT INTO register (memberId,eventId,isPresent) "
					"VALUES (?,?,1)",(memberDict['id'], eventId))
		self.conn.commit()
	
	def setMemberEventPresence(self,memberDict,eventId,isPresent):
		newPresence = 1
		if(isPresent):
			newPresence = 0

	def checkMemberIsPresent(self,memberDict,eventId):
		# return true/false
		pass

	def getMemberForCard(self,cardNum):	
		self.curs.execute("SELECT * FROM members WHERE cardNum=?", (cardNum))
		res = self.curs.fetchone()
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
		self.curs.execute("INSERT INTO members (cardNum, firstName, lastName, hasPaid) "
					"VALUES (?,?,?,?)", insValues)
		self.conn.commit()
