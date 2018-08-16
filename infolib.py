import requests

def getMarket(coin_name):
    if coin_name[0]=='/':
        coin_name=coin_name[1:]
    if coin_name[-4:].upper()=='USDT':
        market=coin_name.upper()
    elif coin_name.upper()=='BTC':
        market='BTCUSDT'
    elif coin_name[-3:].upper()=='BTC':
        market=coin_name.upper()
    else:
        market=coin_name.upper()+'BTC'
    return market

def getInfo(coin_name):
    response=(requests.get("https://api.coingecko.com/api/v3/coins/list")).json()
    coin_id_list=[item['id'] for item in response if item['symbol']==coin_name.lower()]
    msg=''
    for coin_id in coin_id_list:
        response=(requests.get("https://api.coingecko.com/api/v3/coins/"+coin_id)).json()
        msg=msg+"Symbol: "+str(coin_name.upper())+" Name: "+str(response['name'])+"\n"
        msg=msg+"*Community* (Reddit, Facebook, Twitter)"+"\n"
        community_data=response['community_data']
        for key, value in community_data.iteritems():
            msg=msg+"- "+key.replace('_', ' ').title()+": "+str(value)+"\n"
        msg=msg+"*Developer* (Github)"+"\n"
        developer_data=response['developer_data']
        for key, value in developer_data.iteritems():
            msg=msg+"- "+key.replace('_', ' ').title()+": "+str(value)+"\n"
#        msg=msg+"*Market*"+"\n"
#        market_data=response['market_data']
#        for key, value in market_data.iteritems():
#            try:
#                msg=msg+"- "+key.replace('_', ' ')+": "+"{:.8f}".format(float(value))+"\n"
#            except Exception:
#                pass
#            try:
#                msg=msg+"- "+key.replace('_', ' ')+": "+"{:.8f}".format(float(value['btc']))+" btc"+" {:.8f}".format(float(value['usd']))+" usd"+"\n"
#            except Exception:
#                pass
#        msg=msg+"*Misc*"+"\n"
#        for key, value in response.iteritems():
#            try:
#                msg=msg+"- "+key.replace('_', ' ')+": "+"{:.2f}".format(float(value))+"\n"
#            except Exception:
#                pass
        msg=str(msg)
    return msg

