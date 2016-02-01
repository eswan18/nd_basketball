#!/usr/bin/python

import os
import csv
import re

class DataCompleter:
	def complete(self):
		os.makedirs("data/complete_plays")
		for filename in os.listdir("data/raw_plays"):
			print "Completing \"" + filename + "\"..."
			file = open("data/raw_plays/"+filename)
			reader = csv.DictReader(file)
			nd_pos = 0 #variable tracks if ND is home (1) or away (2)
			nd_play_col = ""
			current_lineup = []
			first_half_starters = []
			second_half_starters = []
			for row in reader:
				#On the first row, figure out whether ND is home or away:
				if(nd_pos == 0):
					if(row["home_team"] == "NOTRE DAME"):
						nd_pos = 1
						nd_play_col = "home_play"
					elif(row["away_team"] == "NOTRE DAME"):
						nd_pos = 2
						nd_play_col = "away_play"
					else:
						print "Error"
						break

				#Find lines that denote substitutions:
				nd_play = row[nd_play_col]
				split_in_play = re.split("SUB IN :",nd_play)
				split_out_play = re.split("SUB OUT:",nd_play)

				#Add players to the current lineup when they're subbed in:
				if(len(split_in_play) > 1):
					in_player = split_in_play[1].strip()
					current_lineup.append(in_player)

				#Out substitutions are more complex:
				if(len(split_out_play) > 1):
					out_player = split_out_play[1].strip()
					#If the player was subbed out but was not in the current lineup, record that he is a starter:
					if(out_player not in current_lineup):
						if(int(row["half"]) == 1):
							first_half_starters.append(out_player)
						else:
							second_half_starters.append(out_player)
					#If the player was in the current lineup, just remove him:
					else:
						current_lineup.remove(out_player)

			print first_half_starters
			print second_half_starters
			break




if __name__ == "__main__":
	dataCompleter = DataCompleter()
	dataCompleter.complete()