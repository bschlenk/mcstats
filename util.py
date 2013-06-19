#!/usr/bin/python

import os
import time
import re

_server_dir = '/home/brian/minecraft'
_player_dir = 'world/players'
_log_file = os.path.join(_server_dir, 'server.log')

# used for regex requiring timestamp parsing
timestamp_re = r'\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}'

def timestamp2time(stamp):
	"""Convert minecraft log timestamp to time object."""
	return time.strptime(stamp, "%Y-%m-%d %H:%M:%S")

def get_players():
	"""Return a list of players on the server, based on player.dat files."""
	player_files = os.listdir(os.path.join(_server_dir, _player_dir))
	players = set()
	for player in player_files:
		players.add(os.path.splitext(player)[0])
	return list(players)

class MCLogFile():
	_warn_strs = ['[WARNING]', '[SEVERE]']
	_contents = []

	_login_filter = None
	_logoff_filter = None
	_shutdown_filter = None

	def __init__(self, path=_log_file):
		self._log_file = path
		with open(self._log_file) as f:
			self._contents = [line.strip() for line in f if line]

		login_strings = [r'joined the game', r'.*logged in with.*$']
		logoff_strings = [r'.*lost connection.*$', r'left the game']

		player_regex = '|'.join(get_players())
		filter_base = r'(%s) \[INFO\] (%s)(?:\[.*?\]){,1}' % (timestamp_re, player_regex)
		filter_base += r' (%s)'
		self._login_filter = re.compile(filter_base % '|'.join(login_strings))
		self._logoff_filter = re.compile(filter_base % '|'.join(logoff_strings))
		self._shutdown_filter = re.compile(r'(%s) \[INFO\] Stopping the server' % timestamp_re)

	def __iter__(self):
		return iter(self._contents)

	def info(self):
		for line in self._contents:
			if '[INFO]' in line:
				yield line

	def info_no_convo(self):
		pattern = re.compile(r'^%s \[INFO\] <.*?> .*?$' % (timestamp_re, ))
		for line in self.info():
			if pattern.match(line):
				continue
			else:
				yield line

	def no_warnings(self):
		for line in self._contents:
			if not any(word in line for word in self._warn_strs):
				yield line

	def warnings(self):
		for line in self._contents:
			if any(word in line for word in self._warn_strs):
				yield line

def remove_warnings():
	"""Depricated - use MCLogFile.no_warnings instead
	Remove warnings from the log file."""
	with open("server.log", 'r') as f_in:
		with open("server_filtered.log", 'w') as f_out:
			for line in f_in:
				if not "[WARNING]" in line:
					f_out.write(line)
