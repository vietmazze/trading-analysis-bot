import numpy
from datetime import datetime

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
plt.style.use('classic')
from matplotlib.ticker import FormatStrFormatter
from visuallib import candlestick2_ohlc

def volume_analysis(client,market,num_hours):
    candles=numpy.array(client.get_historical_klines(market,'3m',str(num_hours+1)+' hours ago'),dtype='float')
    closes=[candle[4] for candle in candles]
    volumes=[candle[5] for candle in candles]
    close_min=numpy.amin(closes)
    close_max=numpy.amax(closes)
    close_step=(close_max-close_min)/12
    close_range=[[close_min+(i-1)*close_step,close_min+i*close_step] for i in numpy.arange(1,13)]
    unit_volumes=[]
    unit_closes=[]
    for i in numpy.arange(0,11):
        unit_closes.append(0.5*(close_range[i][0]+close_range[i][1]))
        unit_volume=sum([volumes[j] for j in numpy.arange(0,len(closes)) if close_range[i][0]<=closes[j]<=close_range[i][1]])
        unit_volumes.append(unit_volume)
    index_max=unit_volumes.index(max(unit_volumes))
    return unit_closes,unit_volumes,index_max
    
def getOrderBook(client,market):
    orders=client.get_order_book(symbol=market)
    bids=orders['bids']
    asks=orders['asks']
    bid_prices=[float(bid[0]) for bid in bids]
    bid_qties=[float(bid[1]) for bid in bids]
    ask_prices=[float(ask[0]) for ask in asks]
    ask_qties=[float(ask[1]) for ask in asks] 
    i1=bid_qties.index(max(bid_qties))
    i2=ask_qties.index(max(ask_qties))
    return bid_prices,ask_prices,bid_qties,ask_qties,i1,i2

def trade_analysis_h1(client,market,numTrades):
    toId=client.get_historical_trades(symbol=market,limit=1)[0]['id']
    listId=numpy.arange(toId-numTrades+1,toId-10,500)
    trades=[]
    for fromId in listId:
        trades=trades+client.get_historical_trades(symbol=market,fromId=str(fromId))
    trade_orders=numpy.arange(0,numTrades)  
    trade_days=[datetime.fromtimestamp(int(trade['time']/1000)).day for trade in trades]
    indexes=numpy.unique(trade_days,return_index=True)[1]
    day_counters=[trade_days[index] for index in sorted(indexes)]
    total_coin_buy=[]
    total_coin_sell=[]
    for day_counter in day_counters:
        day_buy_orders=[i for i in trade_orders if trades[i]['isBuyerMaker']==False and datetime.fromtimestamp(int(trades[i]['time']/1000)).day==day_counter]
        day_sell_orders=[i for i in trade_orders if trades[i]['isBuyerMaker']==True and datetime.fromtimestamp(int(trades[i]['time']/1000)).day==day_counter]
        hour_counters=numpy.unique([datetime.fromtimestamp(int(trade['time']/1000)).hour for trade in trades if datetime.fromtimestamp(int(trade['time']/1000)).day==day_counter])
        for hour_counter in hour_counters:
            total_coin_buy.append(sum([float(trades[i]['qty']) for i in day_buy_orders if datetime.fromtimestamp(int(trades[i]['time']/1000)).hour==hour_counter]))
            total_coin_sell.append(sum([float(trades[i]['qty']) for i in day_sell_orders if datetime.fromtimestamp(int(trades[i]['time']/1000)).hour==hour_counter])) 
    total_coin=[x+y for x,y in zip(total_coin_buy,total_coin_sell)]
    return total_coin_buy,total_coin_sell,total_coin

def trade_msg_h1(client,market,numTrades):
    total_coin_buy,total_coin_sell,total_coin=trade_analysis_h1(client,market,numTrades)
    unit_closes,unit_volumes,index_max=volume_analysis(client,market,len(total_coin))
    bid_prices,ask_prices,bid_qties,ask_qties,i1,i2=getOrderBook(client,market)  
    f,(ax1,ax2)=plt.subplots(2,1,gridspec_kw={'height_ratios':[1,1]})
    f.set_size_inches(20,15)
    ax1p=ax1.twiny()
    ax1p.barh(unit_closes,unit_volumes,color='gray',edgecolor='w',height=unit_closes[1]-unit_closes[0],align='center',alpha=0.35)
    ax1p.step(bid_qties,bid_prices,'k',linewidth=1.25,alpha=0.5)
    ax1p.step(ask_qties,ask_prices,'r',linewidth=1.25,alpha=0.5)
    ax1p.set_xticks([])
    for tic in ax1p.xaxis.get_major_ticks():
        tic.tick1On = tic.tick2On = False
        tic.label1On = tic.label2On = False
    candles=numpy.array(client.get_historical_klines(market,'1h','1 month ago'),dtype='float')[-len(total_coin):]
    candlestick2_ohlc(ax1,candles[:,1],candles[:,2],candles[:,3],candles[:,4],width=0.6,alpha=1)
    ax1.yaxis.grid(True)
    for tic in ax1.xaxis.get_major_ticks():
        tic.tick1On = tic.tick2On = False
        tic.label1On = tic.label2On = False
    ax1.set_xticks([])
    ax1.set_xlim(.5,len(total_coin))
    ax1.set_ylim(numpy.amin(candles[:,3]),numpy.amax(candles[:,2]))
    ax1.yaxis.set_major_formatter(FormatStrFormatter('%.8f'))
    ax1.get_yaxis().set_label_coords(-0.075,0.5) 
    ax1.set_ylabel("Volume Profile versus Order Book",fontsize=20)
    ax1.set_title('Exchange: Binance Market: '+market+' Time Frame: 1 [hour]'+' Time Length: '+str(len(candles[:,1]))+' [hours]'+'\nTotal Trades: '+"{:,}".format(numTrades)+' Total Buy Volume: '+"{:,}".format((sum(total_coin_buy)))+' Total Sell Volume: '+"{:,}".format((sum(total_coin_sell)))+"\nCopyright: @trading_analysis_bot",fontsize=25,y=1.03,loc='left')
    candlestick2_ohlc(ax2,numpy.arange(0,len(total_coin)),total_coin,numpy.arange(0,len(total_coin)),total_coin,width=0.6,alpha=.35)
    candlestick2_ohlc(ax2,numpy.arange(0,len(total_coin_buy)),total_coin_buy,numpy.arange(0,len(total_coin_buy)),total_coin_buy,width=0.29,alpha=1,shift=-0.15)
    candlestick2_ohlc(ax2,total_coin_sell,total_coin_sell,numpy.arange(0,len(total_coin_sell)),numpy.arange(0,len(total_coin_sell)),width=0.29,alpha=1,shift=+0.15)
    ax2.yaxis.grid(True)
    for tic in ax2.xaxis.get_major_ticks():
        tic.tick1On = tic.tick2On = False
        tic.label1On = tic.label2On = False
    ax2.set_xticks([])
    ax2.set_xlim(.5,len(total_coin))
    ax2.get_yaxis().set_label_coords(-0.075,0.5) 
    ax2.set_ylabel("Buy versus Sell Volume",fontsize=20)
    ax2.yaxis.set_major_formatter(FormatStrFormatter('%.2f'))
    f.tight_layout()
    plt.savefig(market+'.png',bbox_inches='tight')
    
def trade_analysis_m30(client,market,numTrades):
    toId=client.get_historical_trades(symbol=market,limit=1)[0]['id']
    listId=numpy.arange(toId-numTrades+1,toId-10,500)
    trades=[]
    for fromId in listId:
        trades=trades+client.get_historical_trades(symbol=market,fromId=str(fromId))
    trade_orders=numpy.arange(0,numTrades)  
    trade_days=[datetime.fromtimestamp(int(trade['time']/1000)).day for trade in trades]
    indexes=numpy.unique(trade_days,return_index=True)[1]
    day_counters=[trade_days[index] for index in sorted(indexes)]
    volume_buy_m30=[]
    volume_sell_m30=[]
    for day_counter in day_counters:
        day_buy_orders=[i for i in trade_orders if trades[i]['isBuyerMaker']==False and datetime.fromtimestamp(int(trades[i]['time']/1000)).day==day_counter]
        day_sell_orders=[i for i in trade_orders if trades[i]['isBuyerMaker']==True and datetime.fromtimestamp(int(trades[i]['time']/1000)).day==day_counter]
        hour_counters=numpy.unique([datetime.fromtimestamp(int(trade['time']/1000)).hour for trade in trades if datetime.fromtimestamp(int(trade['time']/1000)).day==day_counter])
        for hour_counter in hour_counters:
            volume_buy_m30.append(sum([float(trades[i]['qty']) for i in day_buy_orders if datetime.fromtimestamp(int(trades[i]['time']/1000)).hour==hour_counter and datetime.fromtimestamp(int(trades[i]['time']/1000)).minute<30]))
            volume_buy_m30.append(sum([float(trades[i]['qty']) for i in day_buy_orders if datetime.fromtimestamp(int(trades[i]['time']/1000)).hour==hour_counter and datetime.fromtimestamp(int(trades[i]['time']/1000)).minute>=30]))
            volume_sell_m30.append(sum([float(trades[i]['qty']) for i in day_sell_orders if datetime.fromtimestamp(int(trades[i]['time']/1000)).hour==hour_counter and datetime.fromtimestamp(int(trades[i]['time']/1000)).minute<30]))
            volume_sell_m30.append(sum([float(trades[i]['qty']) for i in day_sell_orders if datetime.fromtimestamp(int(trades[i]['time']/1000)).hour==hour_counter and datetime.fromtimestamp(int(trades[i]['time']/1000)).minute>=30]))
    volume_m30=[x+y for x,y in zip(volume_buy_m30,volume_sell_m30)]
    if volume_m30[0]==0:
        volume_m30=volume_m30[1:]
        volume_buy_m30=volume_buy_m30[1:]
        volume_sell_m30=volume_sell_m30[1:]
    if volume_m30[-1]==0:
        volume_m30=volume_m30[:-1]
        volume_buy_m30=volume_buy_m30[:-1]
        volume_sell_m30=volume_sell_m30[:-1]
    return volume_buy_m30,volume_sell_m30,volume_m30

def trade_msg_m30(client,market,numTrades):     
    total_coin_buy,total_coin_sell,total_coin=trade_analysis_m30(client,market,numTrades)
    f,(ax1,ax2)=plt.subplots(2,1,gridspec_kw={'height_ratios':[1,1]})
    f.set_size_inches(20,15)
    candles=numpy.array(client.get_historical_klines(market,'30m','1 month ago'),dtype='float')[-len(total_coin):]
    candlestick2_ohlc(ax1,candles[:,1],candles[:,2],candles[:,3],candles[:,4],width=0.6,alpha=1)
    ax1.yaxis.grid(True)
    for tic in ax1.xaxis.get_major_ticks():
        tic.tick1On = tic.tick2On = False
        tic.label1On = tic.label2On = False
    ax1.set_xticks([])
    ax1.set_xlim(.5,len(total_coin))
    ax1.set_ylim(numpy.amin(candles[:,3]),numpy.amax(candles[:,2]))
    ax1.yaxis.set_major_formatter(FormatStrFormatter('%.8f'))
    ax1.get_yaxis().set_label_coords(-0.075,0.5) 
    ax1.set_ylabel("Volume Profile versus Order Book",fontsize=20)
    ax1.set_title('Exchange: Binance Market: '+market+' Time Frame: 30 [minute]'+'\nTotal Trades: '+"{:,}".format(numTrades)+' Total Buy Volume: '+"{:,}".format((sum(total_coin_buy)))+' Total Sell Volume: '+"{:,}".format((sum(total_coin_sell)))+"\nCopyright: @trading_analysis_bot",fontsize=25,y=1.03,loc='left')
    candlestick2_ohlc(ax2,numpy.arange(0,len(total_coin)),total_coin,numpy.arange(0,len(total_coin)),total_coin,width=0.6,alpha=.35)
    candlestick2_ohlc(ax2,numpy.arange(0,len(total_coin_buy)),total_coin_buy,numpy.arange(0,len(total_coin_buy)),total_coin_buy,width=0.29,alpha=1,shift=-0.15)
    candlestick2_ohlc(ax2,total_coin_sell,total_coin_sell,numpy.arange(0,len(total_coin_sell)),numpy.arange(0,len(total_coin_sell)),width=0.29,alpha=1,shift=+0.15)
    ax2.yaxis.grid(True)
    for tic in ax2.xaxis.get_major_ticks():
        tic.tick1On = tic.tick2On = False
        tic.label1On = tic.label2On = False
    ax2.set_xticks([])
    ax2.set_xlim(.5,len(total_coin))
    ax2.get_yaxis().set_label_coords(-0.075,0.5) 
    ax2.set_ylabel("Buy versus Sell Volume",fontsize=20)
    ax2.yaxis.set_major_formatter(FormatStrFormatter('%.2f'))
    f.tight_layout()
    plt.savefig(market+'.png',bbox_inches='tight')