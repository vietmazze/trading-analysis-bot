import urllib,json

def btc_alarm():
    BUY_TOL=20.
    VOL_DIFF=-100.
    url = "https://api.bitfinex.com/v1/trades/btcusd?limit_trades=500"
    trades=json.loads(urllib.urlopen(url).read())
    past_time=trades[0]['timestamp']-5*60  
    buy_volume=[float(trade['amount']) for trade in trades if trade['type']=='buy' and trade['timestamp']>=past_time]
    sell_volume=[float(trade['amount']) for trade in trades if trade['type']=='sell' and trade['timestamp']>=past_time]
    total_buy=int(sum(buy_volume))
    total_sell=int(sum(sell_volume))
    vol_diff=total_buy-total_sell
    msg='Bitfinex BTCUSD (Last 5 mins):\n- Buy volume: '+"{:,}".format(total_buy)+'\n- Sell volume: '+"{:,}".format(total_sell)+')\n- Difference volume: '+"{:,}".format(vol_diff)
    if total_buy<=BUY_TOL and vol_diff<=VOL_DIFF:
        alarm=True
    else:
        alarm=False
    return alarm,msg
