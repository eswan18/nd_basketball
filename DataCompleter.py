#!/usr/bin/python

import os
import csv

class DataCompleter:
	def complete(self):
		os.makedirs("data/complete_plays")
		for filename in os.listdir("data/raw_plays"):
			print "Completing \"" + filename + "\"..."
			file = open("data/raw_plays/"+filename)
			reader = csv.DictReader(file)
			



if __name__ == "__main__":
	dataCompleter = DataCompleter()
	dataCompleter.complete()