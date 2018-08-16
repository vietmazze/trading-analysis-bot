import urllib,csv,urllib2,json

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
plt.style.use('classic')

def crix_index():
    f,ax=plt.subplots(3,1,gridspec_kw={'height_ratios':[1,1,1]})
    f.set_size_inches(15,20)
    ax[0].set_title('CRIX',fontsize=30,y=1.03)
    filename=['crix_hf','crix','crix']
    lengthname=[0,-30,-90]
    labelname=['Intraday [5mins sampl.]','Past month','Past 3 months']
    for i in [0,1,2]:
        response=urllib.urlopen("http://thecrix.de/data/"+filename[i]+".json")
        crix_data=json.loads(response.read())
        crix_value=[data['price'] for data in crix_data]
        ax[i].plot(crix_value[lengthname[i]:],color='b',linewidth=2.5,linestyle='-')
        ax[i].yaxis.grid(True)
        for tic in ax[i].xaxis.get_major_ticks():
            tic.tick1On = tic.tick2On = False
            tic.label1On = tic.label2On = False
        ax[i].set_xticks([])
        ax[i].get_yaxis().set_label_coords(-0.06,0.5) 
        ax[i].set_ylabel(labelname[i],fontsize=20)
        f.tight_layout()
    plt.savefig('crix_index.png',bbox_inches='tight')
    
def bletchley_index():
    f,ax=plt.subplots(3,1,gridspec_kw={'height_ratios':[1,1,1]})
    f.set_size_inches(15,20)
    ax[0].set_title('Bletchley indexes [Past 3 months]',fontsize=30,y=1.03)
    filename=['bletchley_ten','bletchley_twenty','bletchley_forty']
    rank=[10,20,40]
    for i in [0,1,2]:
        cr=csv.reader(urllib2.urlopen('https://www.bletchleyindexes.com/'+filename[i]+'.csv'))
        ib=[]
        for row in cr:
            try:
                ib.append(float(row[3]))
            except Exception:
                pass
        ib=list(reversed(ib[:90]))
        ax[i].plot(ib,linewidth=2.5,linestyle='-')
        ax[i].set_xticks([])
        for tic in ax[i].xaxis.get_major_ticks():
            tic.tick1On = tic.tick2On = False
            tic.label1On = tic.label2On = False
        ax[i].yaxis.grid(True)
        ax[i].get_yaxis().set_label_coords(-0.06,0.5) 
        ax[i].set_ylabel("Bletchley "+str(rank[i]),fontsize=20)
    f.tight_layout()
    plt.savefig('bletchley_index.png',bbox_inches='tight')

