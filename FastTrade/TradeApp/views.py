from django.shortcuts import render
import requests

def index_page(requests):
    tit = "FastTrade"
    return render(requests, 'TradeApp/main.html',{'title':tit})

def auto(requests):
    tit = "FastTrade"
    return render(requests, 'TradeApp/main.html',{'title':tit})