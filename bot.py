import os,psycopg2

import telegram
from telegram import ParseMode
from telegram.ext import Updater,CommandHandler,MessageHandler,Filters

from binance.client import Client

import infolib,tradelib,indexlib,misclib

TOKEN=os.environ['TELEGRAM_TOKEN']

SECRET_KEY=os.environ['SECRET_KEY']
API_KEY=os.environ['API_KEY']
client=Client(API_KEY,SECRET_KEY)

DB_NAME=os.environ['DB_NAME']
DB_USERNAME=os.environ['DB_USERNAME']
DB_HOST=os.environ['DB_HOST']
DB_PASSWORD=os.environ['DB_PASSWORD']
DB_URL="dbname='"+DB_NAME+"' user='"+DB_USERNAME+"' host='"+DB_HOST+"' password='"+DB_PASSWORD+"'"

conn=psycopg2.connect(DB_URL)
cur=conn.cursor()
cur.execute("SELECT chat_id FROM users")
users=cur.fetchall()
id_list=[chat_id[0] for chat_id in users]
cur.close()
conn.close()

ADMIN_ID=os.environ['ADMIN_ID']
ADMIN_USERNAME=os.environ['ADMIN_USERNAME']

def send_msg(bot,update):
    if str(update.message.from_user.username)==ADMIN_USERNAME:
        msg=update.message.text
        if msg[0:19]=='/send_msg markdown ':
            msg=msg[19:]
            for id_item in id_list:
                bot.send_message(chat_id=id_item,text=msg,parse_mode=ParseMode.MARKDOWN)
        if msg[0:15]=='/send_msg html ':
            msg=msg[15:]
            for id_item in id_list:
                bot.send_message(chat_id=id_item,text=msg,parse_mode=ParseMode.HTML)
        if msg[0:14]=='/send_msg img ':
            link=msg[14:]
            bot.send_message(chat_id=update.message.chat_id,text='<img src="'+link+'"/>',parse_mode=ParseMode.HTML)
                
def t(bot,update,args):
    bot.send_chat_action(chat_id=update.message.chat_id,action=telegram.ChatAction.TYPING)
    if args[-1] == '1':
        coin_list=args[:-1]
        opt=1
    else:
        coin_list=args
        opt=0
    for coinName in coin_list:
        market=infolib.getMarket(coinName)
        msg=tradelib.trade_analysis_500(client,market,opt)
        update.message.reply_text(msg,parse_mode=ParseMode.MARKDOWN)
        if opt==1:
            bot.send_photo(chat_id=update.message.chat_id, photo=open(str(market)+'.png', 'rb'))
        if str(update.message.from_user.username)!=ADMIN_USERNAME:
            bot.sendMessage(ADMIN_ID,'chat_id: '+str(update.message.chat_id)+' username: @'+str(update.message.from_user.username)+' market: /'+str(market))

def a(bot,update,args):
    bot.send_chat_action(chat_id=update.message.chat_id,action=telegram.ChatAction.TYPING)
    if args[-1] in ['500','1000','1500','2000','2500','5000','7500','10000','12500','15000','17500','20000','25000','30000','35000','40000','45000','50000']:
        num_trades=int(args[-1])
        coin_list=args[:-1]
    else:
        num_trades=5000
        coin_list=args
    for coinName in coin_list:
        market=infolib.getMarket(coinName)
        tradelib.trade_msg_h1(client,market,num_trades)
        bot.send_photo(chat_id=update.message.chat_id, photo=open(str(market)+'.png', 'rb'))
        tradelib.trade_msg_m30(client,market,num_trades)
        bot.send_photo(chat_id=update.message.chat_id, photo=open(str(market)+'.png', 'rb'))
        if str(update.message.from_user.username)!=ADMIN_USERNAME:
            bot.sendMessage(ADMIN_ID,'chat_id: '+str(update.message.chat_id)+' username: @'+str(update.message.from_user.username)+' market: /'+str(market))
     
def i(bot,update,args):
    bot.send_chat_action(chat_id=update.message.chat_id,action=telegram.ChatAction.TYPING)
    coin_name=args[0].upper()
    msg=infolib.getInfo(coin_name)
    bot.sendMessage(update.message.chat_id,msg,parse_mode=ParseMode.MARKDOWN,disable_web_page_preview=True)
    if str(update.message.from_user.username)!=ADMIN_USERNAME:
        bot.sendMessage(ADMIN_ID,'chat_id: '+str(update.message.chat_id)+' username: @'+str(update.message.from_user.username)+' market: /'+str(coin_name))
        
def m(bot,update):
    bot.send_chat_action(chat_id=update.message.chat_id,action=telegram.ChatAction.TYPING)
    indexlib.bletchley_index()
    bot.send_photo(chat_id=update.message.chat_id, photo=open('bletchley_index.png', 'rb'))
    indexlib.crix_index()
    bot.send_photo(chat_id=update.message.chat_id, photo=open('crix_index.png', 'rb'))
    if str(update.message.from_user.username)!=ADMIN_USERNAME:
        bot.sendMessage(ADMIN_ID,'chat_id: '+str(update.message.chat_id)+' username: @'+str(update.message.from_user.username)+' cmd: indexes')
            
def h(bot,update):
    bot.send_chat_action(chat_id=update.message.chat_id,action=telegram.ChatAction.TYPING)
    misclib.trading_sessions(client)
    bot.send_photo(chat_id=update.message.chat_id, photo=open('trading-sessions.png', 'rb'))
    if str(update.message.from_user.username)!=ADMIN_USERNAME:
        bot.sendMessage(ADMIN_ID,'chat_id: '+str(update.message.chat_id)+' username: @'+str(update.message.from_user.username)+' cmd: h')
                
def manual(bot,update):
    global id_list
    if update.message.chat_id not in id_list:
        id_list.append(update.message.chat_id)
        conn=psycopg2.connect(DB_URL)
        cur=conn.cursor()
        cur.execute("SELECT chat_id FROM users")
        users=cur.fetchall()
        id_list_old=[chat_id[0] for chat_id in users]
        new_id_list=list(set(id_list)-set(id_list_old))
        for new_id in new_id_list:
            db_cmd="INSERT INTO users (chat_id) VALUES ('"+str(new_id)+"')"
            cur.execute(db_cmd)
        conn.commit()
        cur.close()
        conn.close()
        bot.send_message(chat_id=ADMIN_ID,text="ID list: "+str(id_list))
    bot.send_message(chat_id=update.message.chat_id,text="@trading\_analysis\_bot is a Telegram chatbot for data-driven analytics of crypto-market with technical indicators, social sentiment, developer activities and metrics related to crossed-network on-chain transactions. The aim is to assist traders on Binance exchange.\n*Features*\n- Technical indicators: RSI, MA, BB, etc\n- Order flow: buy vs sell, volume profile, limit orderbook\n- Cryptoasset indexes: Bletchley, Bitwise, CRIX\n- Cryptoasset metrics: TX vol, NVT ratio, num active addresses, num transactions\n- Social sentiment and developer activities: Twitter, Reddit, Facebook, GitHub\n- Trading sessions\n- Customized notifications\n*Commands*\n- /a <coin-name-1> <market-name-2> <coin-name-3> <number-of-recent-trades> - Transactions volume versus price statistics. The argument <number-of-recent-trades> can be 500, 1000, 1500, 2000, 2500, 5000, 7500, 10000, 12500, 15000, 17500, 20000, 25000, 30000, 35000, 40000, 45000, 50000 (can be omitted). Examples: /a qtumusdt hot bcn or /a hot npxs btcusdt 20000.\n- /t <coin-name-1> <market-2> <coin-name-3> <chart-flag> - Recent trades summary. If <chart-flag>=1, the volume vs price plot will be provided (can be omitted). Examples: /t hot bat mco 1 or /t npxs btcusdt.\n- /i <coin-name> - Coin information. Examples: /i hot or /i npxs.\n- /m - Market indexes.\n- /h - Trading sesions.\n*Supports*\nIf you don't have a crypto-trading account yet please use the these links to register to [Binance](https://www.binance.com/?ref=13339920) or [Huobi](https://www.huobi.br.com/en-us/topic/invited/?invite_code=x93k3).\nTipjar:\n- BTC: 1DrEMhMP5rAytKyKXRzc6szTcUX8bZzZgq\n- ETH: 0x3915D216f9Fc6ec08f956555e84385513dE5f214\n- LTC: LX8GJkGTZFmAA7puCyVp48333iQdCN6vca\n*Contact*\n@tjeuly",parse_mode=ParseMode.MARKDOWN,disable_web_page_preview=True)
    if str(update.message.from_user.username)!=ADMIN_USERNAME:
        bot.sendMessage(ADMIN_ID,'chat_id: '+str(update.message.chat_id)+' username: @'+str(update.message.from_user.username))

def main():
    updater=Updater(TOKEN)
    dp=updater.dispatcher
    dp.add_handler(CommandHandler("start",manual))
    dp.add_handler(CommandHandler("help",manual))
    dp.add_handler(CommandHandler("a",a,pass_args=True))
    dp.add_handler(CommandHandler("t",t,pass_args=True))
    dp.add_handler(CommandHandler("i",i,pass_args=True))
    dp.add_handler(CommandHandler("m",m))
    dp.add_handler(CommandHandler("h",h))
    dp.add_handler(MessageHandler(Filters.text,send_msg))
    dp.add_handler(MessageHandler(Filters.command,send_msg))
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
