#!/usr/bin/python

import sys
import time
import os
import re
import logging

from util import get_players, MCLogFile, timestamp_re
from util import timestamp2time

login_strings = [r'joined the game', r'.*logged in with.*$']
logoff_strings = [r'.*lost connection.*$', r'left the game']

logging.basicConfig(format='[%(levelname)s] %(message)s', level=logging.DEBUG)

def get_stamp(match_object):
	"""Returns a tuple of player, timestamp based on minecraft log timestamp"""
	player = match_object.group(2)
	timestamp = timestamp2time(match_object.group(1))
	return (player, timestamp)

def get_lists(logfile='server.log'):
	"""Return 2 lists of tuples (player, timestamp) of player logins and logouts,
	and a third list of logout times.
	"""
	if not logfile:
		logfile = 'server.log'

	players = get_players()
	player_regex = '|'.join(players)

	logged_in = []
	logged_out = []
	shutdown = []
	filter_base = r'(%s) \[INFO\] (%s)(?:\[.*?\]){,1}' % (timestamp_re, player_regex)
	filter_base += r' (%s)'
	login_filter = re.compile(filter_base % '|'.join(login_strings))
	logoff_filter = re.compile(filter_base % '|'.join(logoff_strings))
	shutdown_filter = re.compile(r'(%s) \[INFO\] Stopping the server' % timestamp_re)

	mclog = MCLogFile(logfile)
	for line in mclog.info_no_convo():
		result = login_filter.match(line)
		if result:
			logged_in.append(get_stamp(result))
			continue
		result = logoff_filter.match(line)
		if result:
			logged_out.append(get_stamp(result))
			continue
		result = shutdown_filter.match(line)
		if result:
			shutdown.append(timestamp2time(result.group(1)))
	
	return logged_in, logged_out, shutdown
				
def timediff(t1, t2):
	"""Return the difference between two points in time"""
	return abs(time.mktime(t1) - time.mktime(t2)) / 60.

def main():
	logfile = None
	if len(sys.argv) >= 2:
		logfile = sys.argv[1]

	playtimes = {}
	for x in get_players():
		playtimes[x] = 0

	logged_in, logged_out, shutdown = get_lists(logfile)
	for x in logged_in:
		found = False
		for y in logged_out:
			if x[0] == y[0]:
				logging.info("found matching login for %s, %s: %s, %s" %(x[0], time.asctime(x[1]), y[0], time.asctime(y[1])))
				playtimes[x[0]] += timediff(x[1], y[1])
				found = True
				logged_out.remove(y)
				break
		if not found:
			logging.warning("no matching logout for %s, %s" % (x[0], time.asctime(x[1])))

	print playtimes

def attempt_2():
	players = get_players()
	player_regex = '|'.join(players)

	filter_base = r'(%s) \[INFO\] (%s)(?:\[.*?\]){,1}' % (timestamp_re, player_regex)
	filter_base += r' (%s)'
	login_filter = re.compile(filter_base % '|'.join(login_strings))
	logoff_filter = re.compile(filter_base % '|'.join(logoff_strings))
	shutdown_filter = re.compile(r'(%s) \[INFO\] Stopping the server' % timestamp_re)

	actions = {
		'login': login_filter,
		'logoff': logoff_filter,
		'shutdown': shutdown_filter,
	}

	logged_in = {}
	playtimes = {}
	for player in players:
		playtimes[player] = 0

	mclog = MCLogFile()
	for line in mclog.info_no_convo():
		action = None
		for action in actions:
			result = actions[action].match(line)
			if result:
				break
		else:
			continue
		if action == 'login':
			player = result.group(2)
			logging.info('logging in player "%s"' % player)
			if player in logged_in:
				logging.warning('player "%s" already logged in' % player)
				logging.debug(result.group(0))
			else:
				logged_in[result.group(2)] = timestamp2time(result.group(1))
				logging.debug(logged_in.keys())

		elif action == 'logoff':
			player = result.group(2)
			logging.info('logging off player "%s"' % player)
			if player in logged_in:
				playtimes[player] += timediff(logged_in[player], timestamp2time(result.group(1)))
				del logged_in[player]
			else:
				logging.warning('player "%s" was never logged in' % player)
				logging.debug(result.group(0))
			logging.debug(logged_in.keys())

		elif action == 'shutdown':
			logging.info('shutting down')
			shutdown_time = timestamp2time(result.group(1))
			for player in logged_in:
				playtimes[player] += timediff(logged_in[player], shutdown_time)
			logged_in.clear()
			logging.debug(logged_in.keys())
	for player in playtimes:
		print '%s: %f' % (player, playtimes[player])

def simple_log():
	players = get_players()
	player_regex = '|'.join(players)

	filter_base = r'(%s) \[INFO\] (%s)(?:\[.*?\]){,1}' % (timestamp_re, player_regex)
	filter_base += r' (%s)'
	login_filter = re.compile(filter_base % '|'.join(login_strings))
	logoff_filter = re.compile(filter_base % '|'.join(logoff_strings))
	shutdown_filter = re.compile(r'(%s) \[INFO\] Stopping the server' % timestamp_re)

	actions = {
		'login': login_filter,
		'logoff': logoff_filter,
		'shutdown': shutdown_filter,
	}

	mclog = MCLogFile()
	for line in mclog.info_no_convo():
		for action in actions:
			result = actions[action].match(line)
			if result:
				if action == 'shutdown':
					print result.group(1), action
				else:
					print result.group(1), result.group(2), action
		

#main()
#get_lists()
#attempt_2()
simple_log()


