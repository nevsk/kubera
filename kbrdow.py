#!/usr/bin/python

# Dow theory

from datetime import *

dow_debug = True

def debug(msg):
	if dow_debug:
		print msg

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
		self.lowCandlestick = None
		self.highCandlestick = None

	def high(self):
		return self.highCandlestick.high

	def low(self):
		return self.lowCandlestick.low

	def isUpward(self):
		assert len(self.candlesticks) > 2
		if self.lowCandlestick == self.highCandlestick:
			return False
		elif (self.high() < self.low() * 1.06):
			return False
		return self.highCandlestick.date > self.lowCandlestick.date

	def isDownward(self):
		assert len(self.candlesticks) > 2
		if self.lowCandlestick == self.highCandlestick:
			return False
		elif (self.high() < self.low() * 1.06):
			return False
		return self.highCandlestick.date < self.lowCandlestick.date

	def process(self, candlestick):
		candlestick.debug("+\t")
		self.candlesticks.append(candlestick)
		count = len(self.candlesticks)
		if count == 1:
			self.lowCandlestick = candlestick
			self.highCandlestick = candlestick
			return True
		if count > 5:
			if self.isUpward() and (candlestick.low < self.high() * 0.9 or candlestick < self.lowCandlestick) and (self.candlesticks.index(self.highCandlestick) > 4):
				while not self.highCandlestick is self.candlesticks[-1]:
					self.candlesticks[-1].debug("-\t")
					self.candlesticks.pop()
				return False
			elif (self.isDownward()) and (candlestick.high > self.low() * 1.1 or candlestick > self.highCandlestick) and (self.candlesticks.index(self.lowCandlestick) > 4):
				while not self.lowCandlestick is self.candlesticks[-1]:
					self.candlesticks[-1].debug("--\t")
					self.candlesticks.pop()
				return False

		if candlestick > self.highCandlestick:
			self.highCandlestick = candlestick
			candlestick.debug("high\t");
		if candlestick < self.lowCandlestick:
			self.lowCandlestick = candlestick
			candlestick.debug("low\t");
		return True

	def gap(self):
		if self.isUpward():
			return self.high() - self.low()
		else:
			return self.low() - self.high()

	def gapRatio(self):
		if self.isUpward():
			return self.gap() / self.low() * 100
		else:
			return self.gap() / self.high() * 100

	def endDate(self):
		return self.candlesticks[-1].date

	def __xor__(self, other):
		if self.isUpward() and other.isDownward():
			return True
		elif self.isDownward() and other.isUpward():
			return True
		return False

	def __gt__(self, other):
		return self.high() > other.high()

	def __lt__(self, other):
		return self.low() < other.low()


	def period(self):
		return len(self.candlesticks)

	def dump(self):
		if self.period() > 1:
			print "%s-%s\t%5.2f\t%5.2f\t%5.2f (%s)\t%5.2f (%s)\t%3d\t%5.2f(%3d%%)" \
				%(self.candlesticks[0].date.strftime("%Y%m%d"), \
				  self.candlesticks[-1].date.strftime("%Y%m%d"), \
				  self.candlesticks[0].open, self.candlesticks[-1].close, \
				  self.high(), self.highCandlestick.date.strftime("%Y%m%d"), \
				  self.low(), self.lowCandlestick.date.strftime("%Y%m%d"), \
				  self.period(), self.gap(), self.gapRatio())

	def debug(self, msg):
		if dow_debug and self.period() > 1:
			print "%s%s-%s\t%5.2f\t%5.2f\t%5.2f (%s)\t%5.2f (%s)\t%3d\t%5.2f(%3d%%)" \
				%(msg, self.candlesticks[0].date.strftime("%Y%m%d"), \
				  self.candlesticks[-1].date.strftime("%Y%m%d"), \
				  self.candlesticks[0].open, self.candlesticks[-1].close, \
				  self.high(), self.highCandlestick.date.strftime("%Y%m%d"), \
				  self.low(), self.lowCandlestick.date.strftime("%Y%m%d"), \
				  self.period(), self.gap(), self.gapRatio())

# mid to long term trend, last more than 1 month normally
class Trend:
	def __init__(self):
		self.waves = []
		self.waves.append(Wave())
		self.high = self.waves[0]
		self.low = self.waves[0]

	def isUpward(self):
		return self.waves[0].isUpward();

	def isDownward(self):
		return self.waves[0].isDownward();

	def isReversed(self):
		count = len(self.waves)
		if count < 2:
			return False
		if (self.waves[-1].isUpward() and self.isDownward()) or (self.waves[-1].isDownward() and self.isUpward()):
			if abs(self.waves[-1].gap()) > abs(self.waves[-2].gap()):
				debug("big gap")
				return True
		elif self.waves[-1] != self.high and self.waves[-1] != self.low:
			for tmp in self.waves[::-1]:
				if (self.waves[-1].isUpward() and tmp == self.high) or (self.waves[-1].isDownward() and tmp == self.low):
					debug("reversed")
					return True
				elif tmp != self.waves[-1]:
					tmp.debug("remove wave ")
					self.waves.remove(tmp)
		return False

	def process(self, candlestick):
		if not self.waves[-1].process(candlestick):
			if self.isReversed():
				self.waves.pop()
				self.waves.append(Wave())
				return -1
			self.waves.append(Wave())
			return 0
		if self.waves[-1] > self.high:
			self.high = self.waves[-1]
		if self.waves[-1] < self.low:
			self.low = self.waves[-1]
		return 1

	def endDate(self):
		assert len(self.waves) > 0
		assert self.waves[-1].isDone()
		return self.waves[-1].endDate()

	def dump(self):
		for wave in self.waves:
			wave.dump()

	def period(self):
		period = 0
		for wave in self.waves:
			period += wave.period()
		return period

class Movements:
	def __init__(self):
		self.trends = []
		self.trends.append(Trend())

	def process(self, candlestick):
		rc = self.trends[-1].process(candlestick)
		if rc == -1:
			self.trends.append(Trend())
		return rc == 1

	def dump(self):
		print "date\t\t\topen\tclose\thigh\t\t\tlow\t\t\tperiod\tgap"
		for trend in self.trends:
			print "====================================================================="
			trend.dump()
		print "====================================================================="

	def period(self):
		period = 0
		for trend in self.trends:
			period += trend.period()
		return period
