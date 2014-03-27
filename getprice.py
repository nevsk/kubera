#!/usr/bin/python

import stock

stocks = stock.StockPool()
stocks.append("sh600000")
stocks.append("sh600008")
stocks.getCurPrice()
stocks.dump()
