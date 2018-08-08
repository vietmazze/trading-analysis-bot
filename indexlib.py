import urllib,json,numpy

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
plt.style.use('classic')
from visuallib import candlestick2_ohlc

def crix_index(client):
    f,(ax1,ax2,ax3,ax4)=plt.subplots(4,1,gridspec_kw={'height_ratios':[1.5,1,1,1]})
    f.set_size_inches(20,20)
    
    response=urllib.urlopen("http://thecrix.de/data/crix_hf.json")
    crix_data=json.loads(response.read())
    crix_value=[data['price'] for data in crix_data]
    axc=ax1.twinx()
    candles=numpy.array(client.get_historical_klines('BTCUSDT','5m','3 days ago'),dtype='float')[-len(crix_value):]
    candlestick2_ohlc(axc,candles[:,1],candles[:,2],candles[:,3],candles[:,4],width=0.6,alpha=.25)
    axc.set_xticks([])
    for tic in axc.xaxis.get_major_ticks():
        tic.tick1On = tic.tick2On = False
        tic.label1On = tic.label2On = False
    ax1.plot(crix_value,color='b',linewidth=2.5,linestyle='-')
    ax1.yaxis.grid(True)
    for tic in ax1.xaxis.get_major_ticks():
        tic.tick1On = tic.tick2On = False
        tic.label1On = tic.label2On = False
    ax1.set_xticks([])
    ax1.get_yaxis().set_label_coords(-0.06,0.5) 
    ax1.set_ylabel("CRIX [Intraday]",fontsize=20)
    axc.get_yaxis().set_label_coords(1.06,0.5) 
    axc.set_ylabel("BTCUSDT M5",fontsize=20)
    ax1.set_title('The CRypto IndeX (CRIX) provides insight about the current and past movement of the cryptocurrencies market\nThe intraday chart depicts past 24h evolution of the CRIX, updated every 5mins, with current value is '+"{:.2f}".format(crix_value[-1])+"\nCredit: http://thecrix.de\nDisclamer: The CRIX is quite outdated in comparison to the Bletchley index, however still might be useful",fontsize=20,y=1.03,loc='left')
    
    response=urllib.urlopen("http://thecrix.de/data/crix.json")
    crix_data=json.loads(response.read())
    crix_value=[data['price'] for data in crix_data]
    ax2.plot(crix_value[-7:],color='b',linewidth=2.5,linestyle='-')
    ax2.yaxis.grid(True)
    for tic in ax2.xaxis.get_major_ticks():
        tic.tick1On = tic.tick2On = False
        tic.label1On = tic.label2On = False
    ax2.set_xticks([])
    ax2.get_yaxis().set_label_coords(-0.06,0.5) 
    ax2.set_ylabel("CRIX [Past week]",fontsize=20)
    
    ax3.plot(crix_value[-30:],color='b',linewidth=2.5,linestyle='-')
    ax3.yaxis.grid(True)
    for tic in ax3.xaxis.get_major_ticks():
        tic.tick1On = tic.tick2On = False
        tic.label1On = tic.label2On = False
    ax3.set_xticks([])
    ax3.get_yaxis().set_label_coords(-0.06,0.5) 
    ax3.set_ylabel("CRIX [Past month]",fontsize=20)
    
    ax4.plot(crix_value[-90:],color='b',linewidth=2.5,linestyle='-')
    ax4.yaxis.grid(True)
    for tic in ax4.xaxis.get_major_ticks():
        tic.tick1On = tic.tick2On = False
        tic.label1On = tic.label2On = False
    ax4.set_xticks([])
    ax4.get_yaxis().set_label_coords(-0.06,0.5) 
    ax4.set_ylabel("CRIX [Past 3 months]",fontsize=20)
    
    f.tight_layout()
    plt.savefig('crix.png',bbox_inches='tight')

