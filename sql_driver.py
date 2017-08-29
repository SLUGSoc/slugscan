#!/usr/bin/python

import sqlite3

class SqlDriver:

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

    def __init__(self):
       	self.conn = sqlite3.connect('db/slugscan.db')
	self.curs = self.conn.cursor()
	self.setupTables()
        self.conn.commit()
	
    def cleanup(self):
	self.conn.close()

    def queryGetSingle(self,statement,values):
        self.curs.execute(statement, values)
        return self.curs.fetchone()

    def queryWrite(self,statement,values):
        self.curs.execute(statement, values)
        self.conn.commit()

