import numpy
from datetime import datetime

def getMarket(coinName):
    if coinName[0]=='/':
        coinName=coinName[1:]
    if coinName[-4:].upper()=='USDT':
        market=coinName.upper()
    elif coinName.upper()=='BTC':
        market='BTCUSDT'
    elif coinName[-3:].upper()=='BTC':
        market=coinName.upper()
    else:
        market=coinName.upper()+'BTC'
    return market

