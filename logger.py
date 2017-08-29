#!/usr/bin/python

class Logger:

    def __init__(self):
        pass
    
    def out(self, string):
        print string

    def error(self,string):
        print "ERROR: " + string
