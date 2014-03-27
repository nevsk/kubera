#!/usr/bin/python

import urllib2

class Stock:
	def __init__(self, code):
		self.code = code
		self.curPrice = 0
		self.priceChange = 0

	def getCurPrice(self):
		url = 'http://hq.sinajs.cn/?list=%s' % self.code
		req = urllib2.Request(url)
		content = urllib2.urlopen(req).read()
		# data format: name, open, last close, current, high, low, buy price, sell price, volume, tuneover, ...
		data = content.split('"')[1].split(',')
		lastClose = float(data[2])
		self.curPrice = float(data[3])
		self.priceChange = (self.curPrice - lastClose) * 100 / lastClose
		return self.curPrice
