#!/usr/bin/python

import os
from util import get_players

class MCServerError(Exception):
	pass

class MCServer():
	"""Class for getting information about the current minecraft server"""

	#public
	players = []
	files = {
		"server.log": None,
		"whitelist.txt": None,
		"blacklist.txt": None,
		"server.properties": None,
		"ops.txt": None,
	}

	#private
	_root = None

	def __init__(path='.');
		self.refresh_player_list()
		files = os.listdir(path)
		for f in files:
			# check if this folder contains the server
			if f not in self.files:
				raise MCServerError('Could not locate server in directory "%s"' % path)
			self.files[f] = os.path.join(path, f)
		

	def refresh_player_list(self):
		self.players = get_players()
