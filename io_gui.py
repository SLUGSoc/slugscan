#!/usr/bin/env python3

import pygame
import os

class UserPermissionException(Exception):
	pass

S_WIDTH = 800
S_HEIGHT = 480

def center_x(obj_width):
	return (S_WIDTH - obj_width) // 2


def log(string):
	print(string)


def error(e):
	print("ERROR: " + str(e))


def input(prompt):
	string = input(prompt)
	return string


class GUI:

	def __init__(self):
		#pygame.init()
		self.screen = pygame.display.set_mode((S_WIDTH, S_HEIGHT))
		pygame.display.set_caption("SLUGScan")
		pygame.font.init()

		self.bg    = pygame.image.load(os.path.join("gui", "bg.jpg")).convert()
		self.title = pygame.image.load(os.path.join("gui", "slugs_logo.png")).convert_alpha()

		self.fontEvent = pygame.font.SysFont("DejaVu Sans", 48)
		self.fontEvent.set_bold(True)
		self.fontOut   = pygame.font.SysFont("DejaVu Sans", 32)

		self.eventName = ""
		self.outputBuf = ""

		self.textEvent = self.fontEvent.render(self.eventName, 1, (61,61,61))
		self.textOut   = self.fontOut.render(self.outputBuf, 1, (61,61,61))

		pygame.display.toggle_fullscreen()

		self.update()

	def update(self):
		self.screen.fill((0,0,0))
		self.screen.blit(self.bg, (0, 0))
		self.screen.blit(self.title, (center_x(self.title.get_size()[0]), 40))

		self.screen.blit(self.textEvent, (8,424))
		self.screen.blit(self.textOut, (center_x(self.textOut.get_size()[0]), 300))

		pygame.display.flip()

	def output(self, string):
		# Update output text
		self.outputBuf = str(string)
		self.textOut = self.fontOut.render(self.outputBuf, 1, (0,0,0))
		self.update()

	def get_name(self):
		# Throw special exception - name entry not permitted to user
		raise UserPermissionException("Member creation disabled in GUI mode.")

	def show_event(self, ev_name, ev_id):
		# Update the UI's event text
		self.eventName = str(ev_name)
		self.textEvent = self.fontEvent.render(self.eventName, 1, (0,0,0))
		self.update()

	def show_register_update(self, status_change):
		self.output(status_change)