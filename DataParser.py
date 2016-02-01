#!/usr/bin/python

import os
from bs4 import BeautifulSoup
import re
import csv


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
		os.makedirs("data/raw_plays")
		for filename in os.listdir("data/html"):
			self.plays = []
			print "Parsing \"" + filename + "\"...",
			file = open("data/html/"+filename)
			filesoup = BeautifulSoup(file,"html.parser")
			file.close()
			
			#Oddly, this phrase only shows up in the unformatted box scores
			#Use its presence to determine how to parse the file
			#Non-formatted file:
			if("Official Basketball Box Score" in filesoup.get_text()):
				box_score_text = filesoup.find("span",class_ = "presmall").get_text()
				box_score_lines = box_score_text.splitlines()
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
			#Formatted file:
			else:
				# #Get starters:
				# starter_tables = 0
				# #Go through all tables that have "##" to signify a player number column
				# for table in filesoup.find_all("table"):
				# 	if ("##" in table.get_text()):
				# 		starter_tables = starter_tables + 1
				# 		for row in table.find_all("tr"):
				# 			cells = row.find_all("td")
				# 			#check for rows that have c, f, or g (positions) in the position column
				# 			if(len(cells) > 2 and re.match("[cfg]\s*",cells[2].get_text())):
				# 				play = Play()
				# 				if(starter_tables == 1):
				# 					play.home_string = ""
				# 					play.away_string = "SUB IN: "
				# 				else:
				# 					play.home_string = "SUB IN: "
				# 					play.away_string = ""
				# 				play.minute = 20
				# 				play.second = 0

				# 				print "starter:",cells[1].get_text(),cells[2].get_text()
						
				# 	#stop checking after the first 2
				# 	if (starter_tables >= 2):
				# 		break


				#Get the first half play table:
				play_table = filesoup.find("span",class_ = "presmall").find_all("table")[0]
				#initialize the parsing for this file:
				half = 1
				home_score = 0
				away_score = 0
				home_team = None
				away_team = None
				for table_row in play_table.find_all("tr"):
					#Until home and away teams are determined, look for a line beginning with "HOME TEAM:"
					if(home_team is None or away_team is None):
						cells = table_row.find_all("th")
						if (len(cells) > 0 ):
							home_string = cells[0].get_text()
							away_string = cells[4].get_text()
							home_team = re.split("HOME TEAM:\s*",home_string)[1].upper()
							away_team = re.split("VISITORS:\s*",away_string)[1].upper()

					cells = table_row.find_all("td")
					#If the row has 5 cells, parse it as a play:
					if(len(cells) == 5):
						play = Play()
						play.half = half
						play.home_team = home_team
						play.away_team = away_team
						#Deal with half, home team, and away team#########

						#Split the line into useful components:
						play.home_play = cells[0].get_text()
						play.away_play = cells[4].get_text()
						#Split time into minutes and seconds:
						time = cells[1].get_text().strip().split(":")
						play.minute = int(time[0])
						play.second = int(time[1])
						#Split score into home and away
						score = cells[2].get_text().strip().split("-")
						if(len(score) > 1):
							home_score = int(score[0])
							away_score = int(score[1])
						play.home_score = home_score
						play.away_score = away_score
						self.plays.append(play)

				#Get the second half play table:
				play_table = filesoup.find("span",class_ = "presmall").find_all("table")[2]
				half = 2
				for table_row in play_table.find_all("tr"):
					cells = table_row.find_all("td")
					#If the row has 5 cells, parse it as a play:
					if(len(cells) == 5):
						play = Play()
						play.half = half
						play.home_team = home_team
						play.away_team = away_team

						#Split the line into useful components:
						play.home_play = cells[0].get_text()
						play.away_play = cells[4].get_text()
						#Split time into minutes and seconds:
						time = cells[1].get_text().strip().split(":")
						play.minute = int(time[0])
						play.second = int(time[1])
						#Split score into home and away
						score = cells[2].get_text().strip().split("-")
						if(len(score) > 1):
							home_score = int(score[0])
							away_score = int(score[1])
						play.home_score = home_score
						play.away_score = away_score
						self.plays.append(play)

			print "SUCCESS"
			outfilename = filename.split(".")[0] + ".csv"
			print "Writing \"" + outfilename + "\"...",
			self.print_plays(outfilename)
			print "SUCCESS"
	
	#Print plays to a file:
	def print_plays(self, filename):
		file = open("data/raw_plays/"+filename,"w")
		writer = csv.writer(file)
		#Get the names of the object's variables and print them as a header row
		keys = vars(self.plays[0]).keys()
		writer.writerow(keys)
		#For every play, print the variables in appropriate order
		for play in self.plays:
			line_list = []
			for key in keys:
				line_list.append(str(vars(play)[key]))
			writer.writerow(line_list)
		file.close()

