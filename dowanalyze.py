#!/usr/bin/python

import sys
from datetime import *
import time
import kbrdow

def crunch_data(movements, data, index):
	for line in data[index:]:
		# remove \r\n at the end of line
		line = line[:-2]
		items = line.split(',')
		candlestick = kbrdow.Candlestick(date(int(items[0][:4]), int(items[0][4:6]), int(items[0][6:])), float(items[1]), float(items[2]), float(items[3]), float(items[4]))
		if not movements.process(candlestick):
			break
	return movements.period()

movements = kbrdow.Movements()

# remove extra lines
sys.stdin.readline()
sys.stdin.readline()
data = sys.stdin.readlines()
data.pop()

index = 0
while index < len(data) - 1:
	index = crunch_data(movements, data, index)
movements.dump()
