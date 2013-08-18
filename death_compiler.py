#!/usr/bin/python

import re
import sys
import os

def get_players():
	return [os.path.splitext(x)[0] for x in os.listdir('world/players')]

players = get_players()

with open('server.log', 'r') as f:
	regmatch = "(.*?) \[INFO\] ({0}) (.*)".format('|'.join(players))
	prog = re.compile(regmatch)
	chatline = "{0} <{1}> {1} {2}"

	player_deaths = dict((p, 0) for p in players)

	for line in f:
		if not "disconnect" in line and not "lost connection" in line:
			result = prog.match(line)
			if result:
				player = result.group(2)
				player_deaths[player] += 1

	print player_deaths
