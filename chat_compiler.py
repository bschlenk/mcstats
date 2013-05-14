#!/usr/bin/python

import re
import sys

namefilter = ".*?"
if len(sys.argv) == 2:
	namefilter = sys.argv[1]

with open('server.log', 'r') as f:
	regmatch = "(.*?) \[INFO\] <({0})> (.*)".format(namefilter)
	prog = re.compile(regmatch)
	chatline = "{0} <{1}> {2}"

	for line in f:
		result = prog.match(line)
		if result:
			print chatline.format(result.group(1), result.group(2), result.group(3))
