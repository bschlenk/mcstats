#!/usr/bin/python

import os

def get_players():
	"""Return a list of players on the server, based on player.dat files"""
	player_files = os.listdir('world/players')
	players = []
	for x in player_files:
		players.append(os.path.splitext(x)[0])
	return players

def filter_warnings():
	"""Removes warnings from the log file """
	with open("server.log", 'r') as f_in:
		with open("server_filtered.log", 'w') as f_out:
			for line in f_in:
				if not "[WARNING]" in line:
					f_out.write(line)
