import numpy
from datetime import datetime

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
plt.style.use('classic')
from matplotlib.ticker import FormatStrFormatter
from visuallib import candlestick2_ohlc

def trading_sessions(client):
    market_hour=int(str(datetime.fromtimestamp(int(client.get_server_time()['serverTime'])/1000))[-8:-6])
    if market_hour==0:
        market_hour=24
    f,ax=plt.subplots(1,1)
    f.set_size_inches(12,2.5)
    plt.axvspan(xmin=market_hour,xmax=market_hour+1,ymin=0.8,ymax=1,color='gray',facecolor='k',zorder=1,alpha=0.25)
    plt.axhline(y=0.8,linewidth=1,color='k')
    for i in numpy.arange(1,25):
        plt.axvline(x=i,linewidth=1,color='k',zorder=2)
        ax.text(i+0.25,0.86,str(i),fontsize=15)
    plt.axvspan(xmin=7,xmax=16,ymin=0.6,ymax=0.8,color='red',facecolor='k',zorder=3)
    ax.text(7+0.25,0.66,'LONDON',fontsize=15,color='w')
    plt.axvspan(xmin=12,xmax=21,ymin=0.4,ymax=0.6,color='green',facecolor='k',zorder=3)
    ax.text(12+0.25,0.46,'NEW YORK',fontsize=15,color='w')
    plt.axvspan(xmin=21,xmax=25,ymin=0.2,ymax=0.4,color='blue',facecolor='k',zorder=3)
    plt.axvspan(xmin=1,xmax=6,ymin=0.2,ymax=0.4,color='blue',facecolor='k',zorder=3)
    ax.text(21+0.25,0.26,'SYDNEY',fontsize=15,color='w')
    plt.axvspan(xmin=23,xmax=25,ymin=0,ymax=0.2,color='orange',facecolor='k',zorder=3)
    plt.axvspan(xmin=1,xmax=8,ymin=0,ymax=0.2,color='orange',facecolor='k',zorder=3)
    ax.text(23+0.25,0.06,'TOKYO',fontsize=15,color='w')
    for tic in ax.xaxis.get_major_ticks():
        tic.tick1On = tic.tick2On = False
        tic.label1On = tic.label2On = False
    for tic in ax.yaxis.get_major_ticks():
        tic.tick1On = tic.tick2On = False
        tic.label1On = tic.label2On = False
    ax.set_xlim(1,25)
    ax.set_title('Trading sessions (UTC)',fontsize=18)
    f.tight_layout()
    plt.savefig('trading-sessions.png',bbox_inches='tight')