#!/usr/bin/python

import time
import os
import re

from util import get_players, MCLogFile, timestamp_re
from util import timestamp2time

login_strings = [r'joined the game', r'.*logged in with.*$']
logoff_strings = [r'.*lost connection.*$', r'left the game']

def get_stamp(match_object):
	"""Returns a tuple of player, timestamp based on minecraft log timestamp"""
	player = match_object.group(2)
	timestamp = timestamp2time(match_object.group(1))
	return (player, timestamp)

def get_lists():
	"""Returns 2 list of tuples (player, timestamp) of player logins and logouts"""
	players = get_players()
	player_regex = '|'.join(players)

	logged_in = []
	logged_out = []
	filter_base = r'(%s) \[INFO\] (%s)(?:\[.*?\]){,1}' % (timestamp_re, player_regex)
	filter_base += r' (%s)'
	login_filter = re.compile(filter_base % '|'.join(login_strings))
	logoff_filter = re.compile(filter_base % '|'.join(logoff_strings))

	print login_filter.pattern
	print logoff_filter.pattern


	mclog = MCLogFile('server.log')
	for line in mclog.info_no_convo():
		result = login_filter.match(line)
		if result:
			logged_in.append(get_stamp(result))
			continue
		result = logoff_filter.match(line)
		if result:
			logged_out.append(get_stamp(result))
			continue
	
	return logged_in, logged_out
				
def timediff(t1, t2):
	"""Returnst the difference between two points in time"""
	return abs(time.mktime(t1) - time.mktime(t2)) / 60

def main():
	playtimes = {}
	for x in get_players():
		playtimes[x] = 0

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

