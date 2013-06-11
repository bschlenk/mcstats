#!/usr/bin/python

import os
import time
import re

_server_dir = '/home/brian/minecraft'
_player_dir = 'world/players'
_log_file = os.path.join(_server_dir, 'server.log')

# used for regex requiring timestamp parsing
timestamp_re = r"\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}"

def timestamp2time(stamp):
	"""Convert minecraft log timestamp to time object."""
	return time.strptime(stamp, "%Y-%m-%d %H:%M:%S")

def get_players():
	"""Return a list of players on the server, based on player.dat files."""
	player_files = os.listdir(os.path.join(_server_dir, _player_dir))
	players = []
	for player in player_files:
		players.append(os.path.splitext(player)[0])
	return players

class MCLogFile():
	_warn_strs = ['[WARNING]', '[SEVERE]']
	_contents = []

	def __init__(self, path=_log_file):
		self._log_file = path
		with open(self._log_file) as f:
			self._contents = [line.strip() for line in f]
		#self.no_warnings = []
		#self.warnings = []
		#for line in self._contents:
			#if not '[WARNING]' in line:
				#self._contents_no_warning.append(line)
			#else:
				#self.warnings.append(line)
	
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
				return line
		

	def no_warnings(self):
		for line in self._contents:
			if not any(word in line for word in self._warn_strs):
				yield line

	def warnings(self):
		for line in self._contents:
			if '[WARNING]' in line:
				yield line

def remove_warnings():
	"""Depricated - use MCLogFile.no_warnings instead
	Remove warnings from the log file."""
	with open("server.log", 'r') as f_in:
		with open("server_filtered.log", 'w') as f_out:
			for line in f_in:
				if not "[WARNING]" in line:
					f_out.write(line)
