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

	def dump(self):
		print "%8s %.2f %.2f%%" %(self.code, self.curPrice, self.priceChange)

class StockCompoIndex(Stock):
	def getCurPrice(self):
		url = 'http://hq.sinajs.cn/?list=%s' % self.code
		req = urllib2.Request(url)
		content = urllib2.urlopen(req).read()
		# data format: name, current, gap, price change percent, volume, turnover
		data = content.split('"')[1].split(',')
		self.curPrice = float(data[2])
		self.priceChange = float(data[4])

class StockPool:
	def __init__(self):
		self.stocks = []

	def append(self, code):
		self.stocks.append(Stock(code))

	def getCurPrice(self):
		url = 'http://hq.sinajs.cn/?list='
		for stock in self.stocks:
			url += stock.code
			url += ','
		req = urllib2.Request(url)
		content = urllib2.urlopen(req).read()
		index = 0
		for line in content.split("\n"):
			if len(line) == 0:
				break
			data = line.split('"')[1].split(',')
			lastClose = float(data[2])
			self.stocks[index].curPrice = float(data[3])
			self.stocks[index].priceChange = (self.stocks[index].curPrice - lastClose) * 100 / lastClose
			index += 1

	def dump(self):
		for stock in self.stocks:
			stock.dump()
