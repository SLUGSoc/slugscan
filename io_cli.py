#!/usr/bin/python

class CLI:

	def __init__(self):
		pass
	
	def update(self):
		pass

	def setHal(self, halin):
        pass
	
	def output(self, string):
		print string
	
	def log(self, string):
		print string

	def error(self, e):
		print "ERROR: " + str(e)

	def input(self, prompt):
		string = raw_input(prompt)
		return string
	
	def getName(self):
		first = self.input("Enter first name: ")
		last = self.input("Enter last name: ")
		name = {'fst': str(first), 'lst': str(last)}
		return name

	def showEvent(self, evName, evId):
		print("Event Name: " + evName)
		print("Event ID: " + str(evId))

	def showRegisterUpdate(self, statusChange):
		print(statusChange)
	
	def listUnregisteredCards(self, cardList):
		print "Identifier | Card Number | Time"
		for card in cardList:
			print str(card['id']) + " | " + card['cardNum'] + " | " + card['time']

	def getUnregCardId(self):
		string = self.input("Enter Unregistered Card Identifier: ")
		return int(string)
