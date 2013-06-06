#!/usr/bin/python

import os

server_dir = '/home/brian/minecraft'
player_dir = 'world/players'

# used for regex requiring timestamp parsing
timestamp_re = r"\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}"

def timestamp2time(stamp):
	"""Convert minecraft log timestamp to time object."""
	return time.strptime(result.group(1), "%Y-%m-%d %H:%M:%S")

def get_players():
	"""Return a list of players on the server, based on player.dat files."""
	player_files = os.listdir(os.path.join(server_dir, 'world/players'))
	players = []
	for player in player_files:
		players.append(os.path.splitext(player)[0])
	return players

def remove_warnings():
	"""Remove warnings from the log file."""
	with open("server.log", 'r') as f_in:
		with open("server_filtered.log", 'w') as f_out:
			for line in f_in:
				if not "[WARNING]" in line:
					f_out.write(line)
