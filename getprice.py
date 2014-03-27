#!/usr/bin/python

import stock

stock = stock.Stock("sh600000")
stock.getCurPrice()
print "%.2f %.2f%%" %(stock.curPrice, stock.priceChange)
