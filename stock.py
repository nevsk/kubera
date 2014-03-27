#!/usr/bin/python

import urllib2

def getStockPage(stocks):
	url = 'http://hq.sinajs.cn/?list='
	for stock in stocks:
		url += stock.code
		url += ','
	req = urllib2.Request(url)
	return urllib2.urlopen(req).read()

def setStockPrice(stocks, content):
	index = 0
	for line in content.split("\n"):
		# data format: name, open, last close, current, high, low, buy price, sell price, volume, tuneover, ...
		if len(line) == 0:
			break
		data = line.split('"')[1].split(',')
		lastClose = float(data[2])
		stocks[index].curPrice = float(data[3])
		stocks[index].priceChange = (stocks[index].curPrice - lastClose) * 100 / lastClose
		index += 1

class Stock:
	def __init__(self, code):
		self.code = code
		self.curPrice = 0
		self.priceChange = 0

	def getCurPrice(self):
		content = getStockPage(self)
		setStockPrice(self, content)

class StockPool:
	def __init__(self):
		self.stocks = []

	def append(self, code):
		self.stocks.append(Stock(code))

	def getCurPrice(self):
		if len(self.stocks) > 0:
			content = getStockPage(self.stocks)
			setStockPrice(self.stocks, content)

	def dump(self):
		for stock in self.stocks:
			print "%8s %.2f %.2f%%" %(stock.code, stock.curPrice, stock.priceChange)
