#!/usr/bin/python

# Dow theory

from datetime import *

dow_debug = False

# http://stockcharts.com/school/doku.php?id=chart_school:chart_analysis:introduction_to_cand
class Candlestick:
	def __init__(self, date, open, high, low, close):
		self.date = date
		self.open = open
		self.close = close
		self.low = low
		self.high = high

	def isRed(self):
		return self.close > self.open

	def __gt__(self, other):
		return self.high > other.high

	def __lt__(self, other):
		return self.low < other.low

	def __sub__(self, other):
		return self.high - other.low

	def dump(self):
		print "%s\t%.2f\t%.2f\t%.2f\t%.2f" %(self.date.isoformat(), self.open, self.high, self.low, self.close)

	def debug(self, msg):
		if dow_debug:
			print "%s%s\t%.2f\t%.2f\t%.2f\t%.2f" %(msg, self.date.isoformat(), self.open, self.high, self.low, self.close)

# http://stockcharts.com/school/doku.php?id=chart_school:market_analysis:elliott_wave_theory
class Wave:
	def __init__(self):
		self.candlesticks = []
		self.done = False
		self.lowCandlestick = None
		self.highCandlestick = None
		self.less = 0
		self.bigger = 0

	def isUpward(self):
		assert len(self.candlesticks) > 2
		return self.bigger > self.less

	def process(self, candlestick):
		assert not self.done
		candlestick.debug("process ")
		self.candlesticks.append(candlestick)
		count = len(self.candlesticks)
		if count == 1:
			self.lowCandlestick = candlestick
			self.highCandlestick = candlestick
			return True
		if count > 2:
			if self.isUpward() and candlestick.high < self.highCandlestick.high * 0.82:
				while not self.highCandlestick is self.candlesticks[-1]:
					self.candlesticks[-1].debug("pop ")
					self.candlesticks.pop()
				self.done = True
				return False
			elif (not self.isUpward()) and candlestick.low > self.lowCandlestick.low * 1.12:
				while not self.lowCandlestick is self.candlesticks[-1]:
					self.candlesticks[-1].debug("pop ")
					self.candlesticks.pop()
				self.done = True
				return False

		if candlestick > self.candlesticks[0]:
			self.bigger += 1
		elif candlestick < self.candlesticks[0]:
			self.less += 1
		if candlestick > self.highCandlestick:
			self.highCandlestick = candlestick
		if candlestick < self.lowCandlestick:
			self.lowCandlestick = candlestick
		return True

	def period(self):
		return len(self.candlesticks)

	def gap(self):
		if self.isUpward():
			return (self.highCandlestick - self.lowCandlestick) / self.lowCandlestick.low * 100
		else:
			return (self.highCandlestick - self.lowCandlestick) / self.lowCandlestick.high * 100

	def endDate(self):
		return self.candlesticks[-1].date

	def isDone(self):
		return self.done

	def __xor__(self, other):
		if self.isUpward() and not other.isUpward():
			return True
		elif not self.isUpward() and other.isUpward():
			return True
		return False

	def __gt__(self, other):
		return self.highCandlestick.high > other.highCandlestick.high

	def __lt__(self, other):
		return self.lowCandlestick.low > other.lowCandlestick.low

	def dump(self):
		print "%s-%s\t%5.2f\t%5.2f\t%5.2f (%s)\t%5.2f (%s)\t%3d\t%3d%%" \
			%(self.candlesticks[0].date.strftime("%Y%m%d"), \
			  self.candlesticks[-1].date.strftime("%Y%m%d"), \
			  self.candlesticks[0].open, self.candlesticks[-1].close, \
			  self.highCandlestick.high, self.highCandlestick.date.strftime("%Y%m%d"), \
			  self.lowCandlestick.low, self.lowCandlestick.date.strftime("%Y%m%d"), \
			  self.period(), self.gap())

	def count(self):
		return len(self.candlesticks)

# mid to long term trend, last more than 1 month normally
class Trend:
	def __init__(self):
		self.waves = []
		self.waves.append(Wave())
		self.done = False

	def isReversed(self):
		count = len(self.waves)
		if count < 2:
			return False
		if self.waves[-1] ^ self.waves[-2]:
			if self.waves[-1].isUpward() and self.waves[-1] > self.waves[-2]:
				return True
			elif self.waves[-2].isUpward() and self.waves[-1] < self.waves[-2]:
				return True
		return False

	def process(self, candlestick):
		if self.waves[-1].isDone():
			self.waves.append(Wave())

		if not self.waves[-1].process(candlestick):
			if self.isReversed():
				if dow_debug:
					print "pop last wave"
				self.waves.pop()
				self.done = True
			return False
		return True

	def endDate(self):
		assert len(self.waves) > 0
		assert self.waves[-1].isDone()
		return self.waves[-1].endDate()

	def isDone(self):
		return self.done

	def dump(self):
		for wave in self.waves:
			wave.dump()

	def count(self):
		count = 0
		for wave in self.waves:
			count += wave.count()
		return count

class Movements:
	def __init__(self):
		self.trends = []
		self.trends.append(Trend())

	def process(self, candlestick):
		if self.trends[-1].isDone():
			self.trends.append(Trend())

		return self.trends[-1].process(candlestick)

	def dump(self):
		print "date\t\t\topen\tclose\thigh\t\t\tlow\t\t\tperiod\tgap"
		for trend in self.trends:
			trend.dump()

	def count(self):
		count = 0
		for trend in self.trends:
			count += trend.count()
		return count
