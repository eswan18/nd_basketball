#!/usr/bin/python

import urllib2
import shutil
import os

class DataPuller:
	def pull(self,game_count = 1):
		#Remove current data directory and replace with an empty one
		#if(os.path.exists("data")):
		#	shutil.rmtree("data",ignore_errors=True)
		os.makedirs("data/html")

		for x in range(1, game_count + 1):
			attempts = 0
			game_name = self.game_name(x)
			print("Pulling \"" + game_name + "\"..."),
			while attempts < 3:
				if(attempts > 0):
					print("Trying again. Pulling \"" + game_name + "\"..."),
				try:
					url = "http://www.und.com/sports/m-baskbl/stats/2015-2016/"+game_name+".html"
					response = urllib2.urlopen(url)
					content = response.read()
					f = open("data/html/"+game_name+".html",'w')
					f.write(content)
					f.close()
					print "SUCCESS"
					break
				except urllib2.URLError as e:
					print "ERROR"
					attempts += 1
					print type(e)

	#Returns the proper name of the game. Hacky because ND has no consistent naming convention
	def game_name(self,x):
		if(x == 4):
			return "advo3"
		if(x == 5):
			return "advo7"
		if(x == 6):
			return "advo12"
		if(x == 9):
			return "boxscore121315"
		if(x == 10):
			return "xroadg-1"
		if(x == 17):
			return "du0116"
		if(x == 24):
			return "gamebookcu0208"	
		return "game-"+str(x).zfill(2)


if __name__ == "__main__":
	dataPuller = DataPuller()
	dataPuller.pull(25)
