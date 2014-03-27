#!/usr/bin/python

import kbrstock

stocks = kbrstock.StockPool()
stocks.append("sh600000")
stocks.append("sh600008")
stocks.getCurPrice()
stocks.dump()

stock = kbrstock.Stock("sh600009")
stock.getCurPrice()
stock.dump()

index = kbrstock.StockCompoIndex("s_sh000001")
index.getCurPrice()
index.dump()
