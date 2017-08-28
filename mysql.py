#!/usr/bin/python

import ConfigParser
import os

class SqlAccess:
	
	def __init__(self):

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

