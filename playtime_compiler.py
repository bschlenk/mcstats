#!/usr/bin/python

import time
import os
import re

from util import get_players, filter_warnings

def get_stamp(filter, input):
	"""Returns a tuple of player, timestamp based on minecraft log timestamp"""
	result = filter.match(input)
	player = result.group(2)
	timestamp = time.strptime(result.group(1), "%Y-%m-%d %H:%M:%S")
	return (player, timestamp)

def get_lists():
	"""Returns 2 list of tuples (player, timestamp) of player logins and logouts"""
	players = get_players()
	player_regex = '|'.join(players)

	logged_in = []
	logged_out = []
	stamp_filter = re.compile("(.*?) \[INFO\] ({0}).*".format(player_regex))


	with open("server_filtered.log", 'r') as f:
		for line in f:
			if "disconnect." in line:
				logged_out.append(get_stamp(stamp_filter, line))
			if "logged in with" in line:
				logged_in.append(get_stamp(stamp_filter, line))
	
	return logged_in, logged_out
				
def timediff(t1, t2):
	"""Returnst the difference between two points in time"""
	return abs(time.mktime(t1) - time.mktime(t2)) / 60

def main():
	playtimes = {}
	for x in get_players():
		playtimes[x] = 0

	filter_warnings()
	logged_in, logged_out = get_lists()
	for x in logged_in:
		found = False
		for y in logged_out:
			if x[0] == y[0]:
				print "[INFO] found matching login for %s, %s: %s, %s" %(x[0], time.asctime(x[1]), y[0], time.asctime(y[1]))
				playtimes[x[0]] += timediff(x[1], y[1])
				found = True
				logged_out.remove(y)
				break
		if not found:
			print "[WARNING] no matching logout for %s, %s" % (x[0], time.asctime(x[1]))

	print playtimes

main()
