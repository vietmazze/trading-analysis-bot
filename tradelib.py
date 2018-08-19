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

def volume_profile(client,market):
    coinInfo=client.get_symbol_info(market)['filters']
    priceUnit=float(coinInfo[0]['tickSize'])
    units=['5m','15m','30m','1h','4h']
    intervals=['1 day ago','1 week ago','1 month ago','3 months ago','1 year ago']
    infos=['1D','1W','1M','3M','1Y']
    msg='Vol. profile:'
    for k in range(len(units)):
        try:
            candles=numpy.array(client.get_historical_klines(market,units[k],intervals[k]),dtype='float')
            closes=[candle[4] for candle in candles]
            volumes=[candle[5] for candle in candles]
            close_min=numpy.amin(closes)
            close_max=numpy.amax(closes)
            close_step=(close_max-close_min)/24
            close_range=[[close_min+(i-1)*close_step,close_min+i*close_step] for i in numpy.arange(1,25)]
            unit_volumes=[]
            unit_closes=[]
            for i in numpy.arange(0,23):
                unit_closes.append(0.5*(close_range[i][0]+close_range[i][1]))
                unit_volume=sum([volumes[j] for j in numpy.arange(0,len(closes)) if close_range[i][0]<=closes[j]<=close_range[i][1]])
                unit_volumes.append(unit_volume)
            index_max=unit_volumes.index(max(unit_volumes))
            msg=msg+" "+infos[k]+": "+('%.8f' % float(int(numpy.floor(unit_closes[index_max]/priceUnit))*priceUnit)).rstrip('0').rstrip('.')
        except Exception:
            pass
    return msg
    
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
    f,(ax1,ax2)=plt.subplots(2,1,gridspec_kw={'height_ratios':[1,1]})
    f.set_size_inches(20,15)
    ax1p=ax1.twiny()
    ax1p.barh(unit_closes,unit_volumes,color='gray',edgecolor='w',height=unit_closes[1]-unit_closes[0],align='center',alpha=0.35)
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
    ax1.set_ylabel("Volume Profile",fontsize=20)
    ax1.set_title('Exchange: Binance Market: '+market+' Time Frame: 1 [hour]'+' Time Length: '+str(len(candles[:,1]))+' [hours]'+'\nTotal Trades: '+"{:,}".format(numTrades)+' Total Buy Volume: '+"{:,}".format((sum(total_coin_buy)))+' Total Sell Volume: '+"{:,}".format((sum(total_coin_sell))),fontsize=25,y=1.03,loc='left')
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
    bid_prices,ask_prices,bid_qties,ask_qties,i1,i2=getOrderBook(client,market)  
    f,(ax1,ax2)=plt.subplots(2,1,gridspec_kw={'height_ratios':[1,1]})
    f.set_size_inches(20,15)
    ax1p=ax1.twiny()
    ax1p.step(bid_qties,bid_prices,'k',linewidth=2.5,alpha=0.25)
    ax1p.step(ask_qties,ask_prices,'r',linewidth=2.5,alpha=0.25)
    ax1p.set_xticks([])
    for tic in ax1p.xaxis.get_major_ticks():
        tic.tick1On = tic.tick2On = False
        tic.label1On = tic.label2On = False
    candles=numpy.array(client.get_historical_klines(market,'30m','1 month ago'),dtype='float')[-len(total_coin):]
    candlestick2_ohlc(ax1,candles[:,1],candles[:,2],candles[:,3],candles[:,4],width=0.6,alpha=1)
    ax1.yaxis.grid(True)
    for tic in ax1.xaxis.get_major_ticks():
        tic.tick1On = tic.tick2On = False
        tic.label1On = tic.label2On = False
    ax1.set_xticks([])
    ax1.set_xlim(.5,len(total_coin))
    ax1.yaxis.set_major_formatter(FormatStrFormatter('%.8f'))
    ax1.get_yaxis().set_label_coords(-0.075,0.5) 
    ax1.set_ylabel("Order Book",fontsize=20)
    msg=volume_profile(client,market)
    ax1.set_title('Exchange: Binance Market: '+market+' Time Frame: 30 [minute]\n'+msg,fontsize=25,y=1.03,loc='left')
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
    
def trade_analysis_500(client,market,opt):
    trades=client.get_historical_trades(symbol=market)
    minute_counters=[datetime.fromtimestamp(int(trade['time']/1000)).minute for trade in trades]
    market_price=trades[-1]['price']
    market_price=('%.8f' % float(market_price)).rstrip('0').rstrip('.')
    buy_trades=[trade for trade in trades if trade['isBuyerMaker']==False]
    sell_trades=[trade for trade in trades if trade['isBuyerMaker']==True]
    buy_prices=[float(trade['price']) for trade in buy_trades]
    buy_qties=[float(trade['qty']) for trade in buy_trades]
    buy_values=numpy.array([price*qty for price,qty in zip(buy_prices,buy_qties)])
    sell_prices=[float(trade['price']) for trade in sell_trades]
    sell_qties=[float(trade['qty']) for trade in sell_trades]
    sell_values=numpy.array([price*qty for price,qty in zip(sell_prices,sell_qties)])
    if market[-3:]=='BTC':
        n_bot_buy=len(numpy.where(buy_values<0.001)[0])
        n_bot_sell=len(numpy.where(sell_values<0.001)[0])
    else:
        n_bot_buy=-1
        n_bot_sell=-1
    if market[-3:]=='BTC':
        btcPrice=float(client.get_recent_trades(symbol='BTCUSDT')[-1]['price'])
        buy_values=buy_values*btcPrice
        sell_values=sell_values*btcPrice
    total_buy=int(sum(buy_values))
    total_sell=int(sum(sell_values))
    n_buy=len(buy_values)
    n_sell=len(sell_values)
    sig_buy=[]
    sig_sell=[]
    thresholds=[100,200,500,1000,2000,5000,10000]
    for threshold in thresholds:
        sig_buy.append(len(numpy.where(buy_values>threshold)[0]))
        sig_sell.append(len(numpy.where(sell_values>threshold)[0]))
    n_buy_small=len(numpy.where(buy_values<10)[0])
    n_sell_small=len(numpy.where(sell_values<10)[0])
    time_duration='From '+str(datetime.fromtimestamp(int(trades[0]['time'])/1000))+' to '+str(datetime.fromtimestamp(int(trades[-1]['time'])/1000))+' (UTC)'
    msg='#'+market+': '+market_price+'\n*Transactions statistics* (Last 500 trades)\n'+time_duration
    msg=msg+'\n~ 0$: Buy '+str(n_bot_buy)+' vs Sell '+str(n_bot_sell)
    msg=msg+'\n~ 1-10$: Buy '+str(n_buy_small-n_bot_buy)+' vs Sell '+str(n_sell_small-n_bot_sell)
    for i in numpy.arange(0,len(thresholds),1):
        msg=msg+'\n> '+"{:,}".format(thresholds[i])+'$: Buy '+str(sig_buy[i])+' vs Sell '+str(sig_sell[i])
    msg=msg+'\nTotal: Buy '+str(n_buy)+' ('+"{:,}".format(total_buy)+'$) vs Sell '+str(n_sell)+' ('+"{:,}".format(total_sell)+'$)'
    trade_prices=[float(trade['price']) for trade in trades]
    trade_orders=numpy.arange(0,500)
    buy_orders=[i for i in trade_orders if trades[i]['isBuyerMaker']==False]
    sell_orders=[i for i in trade_orders if trades[i]['isBuyerMaker']==True]
    if opt==1:
        f,ax=plt.subplots(1,1)
        f.set_size_inches(20,5) 
        ax.bar(buy_orders,buy_qties,color='g',edgecolor='g',width=0.9,align='center',alpha=0.75,label='Buy quantities')
        ax.bar(sell_orders,sell_qties,color='r',edgecolor='r',width=0.9,align='center',alpha=0.75,label='Sell quantities')
        ax.get_yaxis().set_label_coords(-0.075,0.5) 
        ax.set_ylabel("Trade volumes",fontsize=20)
        axt=ax.twinx()
        axt.step(trade_orders,trade_prices,color='b',linewidth=2,linestyle='-',label='Trade prices')
        axt.set_ylabel("Trade prices",fontsize=20)
        axt.get_yaxis().set_label_coords(1.075,0.5)
        axs=ax.twinx()
        axs.step(trade_orders,minute_counters,color='violet',linewidth=2,alpha=.5,linestyle='-',label='Time minute counters')
        axs.set_yticks([])
        ax.set_xlim(0,500)
        ax.yaxis.grid(True)
        for tic in ax.xaxis.get_major_ticks():
            tic.tick1On = tic.tick2On = False
            tic.label1On = tic.label2On = False
        ax.yaxis.set_major_formatter(FormatStrFormatter('%.2f'))
        axt.yaxis.set_major_formatter(FormatStrFormatter('%.8f'))
        ax.set_title(str(market),fontsize=20,loc='left',y=1.03)
        ax.legend(loc='upper left', bbox_to_anchor=(0.3, 1.15), shadow=True, fontsize='x-large', ncol=2)
        axt.legend(loc='upper left', bbox_to_anchor=(0.634, 1.15), shadow=True, fontsize='x-large', ncol=2)
        axs.legend(loc='upper left', bbox_to_anchor=(0.783, 1.15), shadow=True, fontsize='x-large', ncol=1)
        f.tight_layout()
        plt.savefig(market+'.png',bbox_inches='tight')
    return msg
    
