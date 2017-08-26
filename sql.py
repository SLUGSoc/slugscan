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
					"id 		INT, " 
					"cardNum 	CHARACTER(20)	UNIQUE NOT NULL, "
					"firstName 	NVARCHAR(32)	NOT NULL, "
					"lastName 	NVARCHAR(32)	NOT NULL, "
					"alias		NVARCHAR(32)	, "
					"hasPaid 	BOOLEAN		DEFAULT 1,"
					"PRIMARY KEY (id ASC) "
					")")
		self.curs.execute("CREATE TABLE IF NOT EXISTS events ("
					"id		INT, "
					"name		NVARCHAR(32)	UNIQUE NOT NULL, "
					"PRIMARY KEY (id ASC) "
					")")
		self.curs.execute("CREATE TABLE IF NOT EXISTS register ("
					"memberId	INT, "
					"eventId	INT, "
					"isPresent	BOOLEAN		DEFAULT 0, "
					"FOREIGN KEY(memberId) 	REFERENCES members(id), "
					"FOREIGN KEY(eventId) 	REFERENCES events(id) "
					")")
	
	def getCurrentEvent(self, eventName):
		# get current event id, by finding event of same name, or by creating if non-existent
		pass

	def __init__(self, eventName):
		self.conn = sqlite3.connect('slugscan.db')
		self.curs = self.conn.cursor()
		self.setupTables()
		self.eventId = self.getCurrentEvent(eventName)
		self.conn.commit()
	
	def cleanup(self):
		self.conn.close()

	def getEventIdByName(eventName):
		pass

	def addMemberToEvent(memberId,eventId):
		pass
	
	def setMemberEventPresence(memberId,eventId,isPresent):
		newPresence = 1
		if(isPresent):
			newPresence = 0

	def checkMemberIsPresent(self,memberId,eventId):
		# return true/false
		pass

	def getMemberForCard(self,cardNum):	
		self.curs.execute('SELECT * FROM members WHERE cardNum=?', [cardNum])
		res = self.curs.fetchone()
		# return memberId, names as dictionary
		if (res is None):
			raise NoMemberException("No member exists in database!")
		else:
			# TODO return data
			return

	def createMember(self,cardNum,firstName,lastName,isPaidMember=True):
		# exception if unsuccessful
		hasPaid = 0
		if (isPaidMember):
			hasPaid = 1
		insValues = (cardNum,firstName,lastName,hasPaid)
		self.curs.execute("INSERT INTO members (cardNum, firstName, lastName, hasPaid) VALUES (?,?,?,?)", insValues)
		self.conn.commit()
