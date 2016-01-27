#!/usr/bin/python

import os
from bs4 import BeautifulSoup
import re


class Play:
	def init(self):
		self.half = -1
		self.minute = -1
		self.second = -1
		self.home_play = None
		self.away_play = None
		self.home_score = 0
		self.away_score = 0
		self.home_team = None
		self.away_team = None
		
class DataParser:
	def parse(self):
		self.plays = []
		for filename in os.listdir("data"):
			file = open("data/"+filename)
			filesoup = BeautifulSoup(file,"html.parser")
			file.close()
			
			#Oddly, this phrase only shows up in the unformatted box scores
			#Use its presence to determine how to parse the file:
			if("Official Basketball Box Score" in filesoup.get_text()):
				box_score_text = filesoup.find("span",class_ = "presmall").get_text()
				box_score_lines = box_score_text.splitlines()
				print "Parsing \"" + filename + "\"...",
				#initialize the parsing for this file:
				is_play = False
				half = 0
				home_score = 0
				away_score = 0
				home_team = None
				away_team = None

				#Parse line by line:
				for line in box_score_lines:
					
					#Until home and away teams are determined, look for a line beginning with "HOME TEAM:"
					if(home_team is None or away_team is None):
						if(re.match("HOME TEAM:",line)):
							#The home and away team columns are separated by time, score, and margin
							team_strings = re.split("\s*TIME\s*SCORE\s*MAR\s*",line)
							home_string = team_strings[0]
							away_string = team_strings[1]
							home_team = re.split("HOME TEAM:\s*",home_string)[1].upper()
							away_team = re.split("VISITORS:\s*",away_string)[1].upper()
							is_play = False

					#blank lines denote the end of a half:
					if(len(line) == 0):
						is_play = False

					#Parse plays and put them into play objects:
					if(is_play):
						play = Play()
						play.half = half
						play.home_team = home_team
						play.away_team = away_team
						
						#Get the time:
						time = re.search("[0-2][0-9]:[0-5][0-9]",line)
						time_components = time.group().split(":")#split into minutes and seconds
						play.minute = int(time_components[0])
						play.second = int(time_components[1])

						#Split the line into halves, using the time as a separator:
						two_component_split = re.split("[0-2][0-9]:[0-5][0-9]", line)
						left = two_component_split[0].strip()
						right = two_component_split[1].strip()

						#The left side is just the home play description
						play.home_play = left

						#The right side is [the current score], [the margin], the away play description
						#Check for the score:
						score = re.match("[0-2]?[0-9]?[0-9]-[0-2]?[0-9]?[0-9]",right)
						#If this line matches the regex for a score, update the home and away scores:
						if(score):
							scores = score.group(0).split("-")#split into home and away scores
							home_score = int(scores[0])
							away_score = int(scores[1])
						play.home_score = home_score
						play.away_score = away_score
						
						#Remove the score and margin from the right string, leaving you with the away play:
						right_split = re.split("[0-2]?[0-9]?[0-9]-[0-2]?[0-9]?[0-9]\s*[VHT] \d{1,3}\s*", right, maxsplit = 1)
						if(len(right_split) > 1):
							right = right_split[1]#update the right
						play.away_play = right

						#Add this play to the list of plays
						self.plays.append(play)

					#lines of dashes denote the beginning of a half:
					if(len(line) > 0 and line[0] == "-"):
						is_play = True
						half = half + 1
			
			print "SUCCESS"
		self.print_plays()
	
	def print_plays(self):
		count = 0
		for play in self.plays:
			print "Play " + str(count) + " happened at " + str(play.minute) + ":" + str(play.second)
			print "The score was " + str(play.home_score) + " to " + str(play.away_score)
			print "And here's what happened:"
			print play.home_team + ":" + play.home_play + ";"
			print play.away_team + ":" + play.away_play + ";\n"
			count = count + 1

