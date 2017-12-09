#!/usr/bin/python

import RPi.GPIO as GPIO
import time

class GPIOAccess:

	def __init__(self):
		GPIO.setmode(GPIO.BOARD)

		# GPIO Pin definitions
		
		self.p_led = [13,19]
		self.p_led[0] = 13 # Green
		self.p_led[1] = 19 # Red
		self.p_buzzer = 22		
		GPIO.setup(self.p_led[0], GPIO.OUT)
		GPIO.setup(self.p_led[1], GPIO.OUT)
		GPIO.setup(self.p_buzzer, GPIO.OUT)
		
		# Set all on
		GPIO.output(self.p_led[0], True)	
		GPIO.output(self.p_led[1], True)	
		GPIO.output(self.p_buzzer, True)	
		
		time.sleep(1)

		# Set all off
		GPIO.output(self.p_led[0], False)	
		GPIO.output(self.p_led[1], False)	
		GPIO.output(self.p_buzzer, False)	

		pass
	
	def update(self):
		pass

	def buzz(self, duration, waitTime):
		GPIO.output(self.p_led[0], True)	
		GPIO.output(self.p_buzzer, True)	
		
		time.sleep(duration)

		GPIO.output(self.p_led[0], False)	
		GPIO.output(self.p_buzzer, False)
		
		time.sleep(waitTime)
	
	def successfulScan(self):
		self.buzz(0.5, 0.01)
	
	def notRegistered(self):
		self.buzz(0.1, 0.1)
		self.buzz(0.1, 0.1)
		self.buzz(0.1, 0.1)
		self.buzz(0.1, 0.1)
		self.buzz(0.1, 0.1)

	def halTalks(self):
		self.buzz(0.1, 0.1)
		self.buzz(0.08, 0.08)
		self.buzz(0.08, 0.1)
		self.buzz(0.12, 0.01)
