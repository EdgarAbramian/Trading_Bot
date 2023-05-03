from django.shortcuts import render
import requests
from binance.client import Client
import pandas as pd
import numpy as np
import time
from tradingview_ta import TA_Handler, Interval, Exchange
# from .models import UserInfo
from django.shortcuts import redirect 

api_key = 'V9GyIlfInl8eO3TKpVOXb13gvXs78ozMvKZC3xOpIIepfoYmXCgXhojazGwNWQK7'
api_secret = 'lAqnVmsseWXmcnDcceeC2tkjqoZXbiqKdxo5hD3hSOnZIfL7MgccYoSkvUln6DqY' 
COIN_LINK= 'https://www.binance.com/ru/futures/'
ASSET = []
#СОЗДАНИЕ КЛИЕНТА
client = Client(api_key, api_secret)

# def buy(requests):
#     api = requests.POST.get('api', False) 
#     secret = requests.POST.get('secret', False) 
#     a = UserInfo.objects.all()
#     newuser = UserInfo(api = api,secret = secret) 
#     newuser.save()
#     print('---------------------------------')
    
#     apikey = (a[len(a)-1].api)
#     apisecret = (a[len(a)-1].secret)
#     print('---------------------------------')
    
#     return render(requests, 'TradeApp/main.html',{'title':"FastTrade",'api':api,'sec':secret})


#ПОДБИРАЕМ КРИПТУ
#Interval.INTERVAL_15_MINUTES
def top_coin(INTERVAL):
   client = Client(api_key, api_secret)
   all_tickers = pd.DataFrame(client.get_ticker())
   asset = all_tickers[all_tickers.symbol.str.contains('USDT')]
   for i in asset['symbol']:
        try:
            handler = TA_Handler(
                    screener="crypto",
                    interval= INTERVAL,
                    symbol = i,
                    exchange="binance",
                )
            
            analysis = handler.get_analysis().summary
            if (analysis['RECOMMENDATION'] == 'BUY'):

                return {'coin':i,
                        'analysis':analysis,
                        'RSI':handler.get_indicators()['RSI'],
                        'MACD':handler.get_indicators()['MACD.signal'],
                        'volume':handler.get_indicators()['volume'],
                        'SMA10':handler.get_indicators()['SMA10'],}
        except:
            Exception

def index_page(requests):
    return render(requests, 'TradeApp/main.html',{'title':"FastTrade"})

def auto(requests):
    return render(requests, 'TradeApp/auto.html',{'title': "AUTO"})

def rec_long(requests):
    res = top_coin(Interval.INTERVAL_1_MONTH)
    ASSET.append(res["coin"])
    return render(requests, 'TradeApp/rec.html',{'INTERVAL':"LONG",'COIN':res["coin"],'BUY':res['analysis']['BUY'],'SELL':res['analysis']['SELL']})

def rec_short(requests):
    res = top_coin(Interval.INTERVAL_15_MINUTES)
    ASSET.append(res["coin"])
    return render(requests, 'TradeApp/short.html',{'INTERVALs':"SHORT",'COINs':res["coin"],'BUYs':res['analysis']['BUY'],'SELLs':res['analysis']['SELL']})

def rec(requests):
    return render(requests, 'TradeApp/rec.html')

def LINK_TO_COIN(requests,):
    response = redirect(COIN_LINK + ASSET[-1]) 
    return response





