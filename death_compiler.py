#!/usr/bin/python

import re
import sys
import os

from util import get_players

# Death message example
# 2013-04-24 11:40:24 [INFO] HiFriendHi was slain by Spider

players = get_players()
timestamp_re = r"\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}"

ignore_list = [
	"lost connection",
	"joined the game",
	"left the game",
]

def get_death_dict():
	death_strings = set()
	with open('server.log', 'r') as f:
		regmatch = "({0}) \[INFO\] ({1}) (?!.*{2}.*)(.*)".format(timestamp_re, '|'.join(players), '|'.join(ignore_list))
		prog = re.compile(regmatch)

		player_deaths = dict((p, 0) for p in players)

		for line in f:
			result = prog.match(line)
			if result:
				player = result.group(2)
				player_deaths[player] += 1
				death_strings.add(result.group(3))

	return player_deaths

deaths = get_death_dict()
if len(sys.argv) >= 2:
	player = sys.argv[1]
	try:
		print deaths[player]
	except KeyError:
		print "%s is not a valid player." % player
else:
	for player, death in deaths.iteritems():
		print "%s: %d" % (player, death)
