# Trading Analysis Bot

[![Dependencies](https://img.shields.io/badge/dependencies-talib-brightgreen.svg)](http://mrjbq7.github.io/ta-lib/)
[![License](https://img.shields.io/badge/license-MIT-blue.svg)](https://opensource.org/licenses/MIT)

## Requirements

- Telegram library: python-telegram-bot
- Exchange library: python-binance
- Computational libraries: numpy, TA-lib
- Visualization library: matplotlib
- Database library: psycopg2

## Features

- Standard technical indicators
- Order flow trading
- Market indexes and rankings
- Social network sentiment
- Developer activities
- Trading sessions
- Customized notifications
- Admin and user management

## Run on local machine

```
pip install -r requirements.txt
pip install TA-lib
```

```
# For Windows
set TELEGRAM_TOKEN=XXXXXXXXXXXXXXXXXXXXXXXXXXXXXX 
set SECRET_KEY=XXXXXXXXXXXXXXXXXXXXXXXXXXXXXX 
set API_KEY=XXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
set DB_NAME=XXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
set DB_USERNAME=XXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
set DB_HOST=XXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
set DB_PASSWORD=XXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
set ADMIN_ID=XXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
set ADMIN_USERNAME=XXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
python bot.py
```

```
# For Linux
export TELEGRAM_TOKEN=XXXXXXXXXXXXXXXXXXXXXXXXXXXXXX 
export SECRET_KEY=XXXXXXXXXXXXXXXXXXXXXXXXXXXXXX 
export API_KEY=XXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
export DB_NAME=XXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
export DB_USERNAME=XXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
export DB_HOST=XXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
export DB_PASSWORD=XXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
export ADMIN_ID=XXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
export ADMIN_USERNAME=XXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
python bot.py
```

## Deployment on Heroku platform

```
heroku create --region eu vozbot 
heroku buildpacks:add --index 1 heroku/python
heroku buildpacks:add --index 2 https://github.com/numrut/heroku-buildpack-python-talib
heroku config:set TELEGRAM_TOKEN=XXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
heroku config:set SECRET_KEY=XXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
heroku config:set API_KEY=XXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
heroku config:set DB_NAME=XXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
heroku config:set DB_USERNAME=XXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
heroku config:set DB_HOST=XXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
heroku config:set DB_PASSWORD=XXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
heroku config:set ADMIN_ID=XXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
heroku config:set ADMIN_USERNAME=XXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
git push heroku master
heroku ps:scale bot=1 
```

## Screenshots

### General information
```
/i npxs
```
```
Symbol: NPXS Name: Pundi X
*Community*
- reddit accounts active 48h: 51
- twitter followers: 40273
- reddit subscribers: 2342
- reddit average posts 48h: 0.955
- reddit average comments 48h: 15.5
- facebook likes: 107214
*Developer*
- pull requests merged: 0
- commit count 4 weeks: 0
- stars: 1
- total issues: 0
- subscribers: 0
- pull request contributors: 0
- forks: 1
- closed issues: 0
*Market*
- ath change percentage: -83.87082275 btc -87.38840617 usd
- circulating supply: 101102252411.49507141
- price change percentage 7d in currency: -6.76702839 btc -24.15269053 usd
- price change percentage 60d in currency: -72.10525512 btc -76.75106923 usd
- current price: 0.00000029 btc 0.00182400 usd
- price change percentage 60d: -76.75106923
- low 24h: 0.00000028 btc 0.00174536 usd
- market cap change percentage 24h: -16.85483411
- price change percentage 1y: 0.00000000
- price change percentage 200d: 0.00000000
- ath: 0.00000179 btc 0.01446299 usd
- total volume: 1360.67323203 btc 8573900.96211540 usd
- market cap change 24h in currency: -3796.08654186 btc -37382901.31112948 usd
- price change percentage 7d: -24.15269053
- price change percentage 30d in currency: -52.63038921 btc -55.45402743 usd
- price change percentage 14d in currency: -17.37003225 btc -38.17597396 usd
- market cap change 24h: -37382901.31113000
- price change percentage 30d: -55.45402743
- price change percentage 24h: -16.85483411
- price change percentage 24h in currency: -11.48174844 btc -16.85483411 usd
- market cap change percentage 24h in currency: -11.48174844 btc -16.85483411 usd
- price change 24h in currency: -0.00000004 btc -0.00036975 usd
- price change percentage 14d: -38.17597396
- price change 24h: -0.00036975
- high 24h: 0.00000034 btc 0.00226542 usd
- market cap: 29265.83396764 btc 184410449.25842109 usd
*Misc*
- coingecko score: 41.47
- community score: 43.30
- public interest score: 28.78
- coingecko rank: 178.00
- market cap rank: 49.00
- developer score: 12.00
- liquidity score: 48.92
```

### Order flow trading
```
/a wpr 2500
```
<img src="img/a_wpr_2500_h1.png" width="700">
<img src="img/a_wpr_2500_m30.png" width="700">

### Market indexes
```
/ic
```
<img src="img/ic.png" width="700">

### Trading sessions
```
/h
```
<img src="img/h.png" width="700">

## Licence
MIT

## Support and Donation

- Star and/or fork this repository
- Trade on Binance: https://www.binance.com/?ref=13339920
- Trade on Huobi: https://www.huobi.br.com/en-us/topic/invited/?invite_code=x93k3
- BTC: 1DrEMhMP5rAytKyKXRzc6szTcUX8bZzZgq
- ETH: 0x3915D216f9Fc6ec08f956555e84385513dE5f214
- LTC: LX8GJkGTZFmAA7puCyVp48333iQdCN6vca
