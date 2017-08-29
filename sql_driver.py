#!/usr/bin/python

import sqlite3
import ConfigParser
import os

class SqlDriver:

	def getMySqlConfig(self):
		# Import config 
		config = ConfigParser.ConfigParser()
		config.readfp(open(r'db/slugscan.cfg'))

		# Parse MySQL config
		sqlUser = config.get('MySQL', 'username')
		sqlPass = config.get('MySQL', 'password')
		sqlHost = config.get('MySQL', 'host')
		sqlDb	= config.get('MySQL', 'db')

		sqlConfig = {
			'user':		sqlUser,
			'passwd': 	sqlPass,
			'host':		sqlHost,
			'db':		sqlDb
		}
		return sqlConfig

	def setupTables(self):
		self.log.out("Preparing SQL tables...")
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
		self.conn.commit()
		self.log.out("SQL tables prepared")

	def __init__(self, logger):
		self.conn = sqlite3.connect('db/slugscan.db')
		self.curs = self.conn.cursor()
		self.log = logger
		self.setupTables()

	def cleanup(self):
		self.conn.close()

	def queryGetSingle(self,statement,values):
		self.curs.execute(statement, values)
		return self.curs.fetchone()

	def queryWrite(self,statement,values):
		self.curs.execute(statement, values)
		self.conn.commit()

