#!/usr/bin/python

import time
import datetime
from datetime import date

from bs4 import BeautifulSoup as Soup
import urllib2
import csv

# set up dates
startTS = time.time()
todayDate = date.today()
pastDate = datetime.date(2014, 10, 28)

# initialize result collections
teamArray = []
scoreArray = []

# loop from first game of 2014 season to today
while (pastDate != todayDate):

	# load nba scoreboard webpage
	dateStr = pastDate.strftime('%Y%m%d') #20141028
	soup = Soup(urllib2.urlopen('http://www.nba.com/gameline/' + dateStr))

	# select nba team names and scores
	teams = soup.find_all('div', { "class" : "nbaModTopTeamName"})
	scores = soup.find_all('div', { "class" : "nbaModTopTeamNum"})
	for t in teams:
		teamArray.append(t.string)
	for s in scores:
		scoreArray.append(s.string)

	# go to next date
	pastDate += datetime.timedelta(days=1)


# write results to spreadsheet
todayDateStr = todayDate.strftime('%Y%m%d')
with open('nbaScores2014-' + todayDateStr + '.tsv', 'w') as csvfile:
	writer = csv.writer(csvfile, delimiter='\t',
		quotechar='|', quoting=csv.QUOTE_MINIMAL)

	writer.writerow(('Team1', 'Score1', 'Team2', 'Score2'))
	for i in range(0, len(teamArray), 2):
		writer.writerow((teamArray[i], scoreArray[i], teamArray[i+1], scoreArray[i+1]))


# print how long code took to execute
print 'Done! ' + str('%.2f' % (time.time() - startTS)) + ' seconds'