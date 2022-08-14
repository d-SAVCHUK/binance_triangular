import requests
import json
from config import API_KEY, API_SECRET, base
from binance.client import Client
import pandas as pd
import csv
import re

ping = "/api/v3/ping"
price = '/api/v3/ticker/price'

url1 = base + ping
r = requests.get(url1)

print('server response', r)

if r.status_code == 200:
    print('Ok', r.json())
else:
    print("error")

url2 = base + price
file = requests.get(url2) #download info from exchange in json file
h = file.json()
print('numbers of tickers are:', len(h)-1)

db = pd.DataFrame(h)
new_db = db.insert(1, "symbol2", value=db["symbol"]) #add of column
db.columns = ["Base Asset", "Quote Asset", "Price"]  #rename of columns
db2 = db.replace(to_replace={"Base Asset":
                                 {r'BTC$', r'ETH$', r'USDT$', r'BNB$', r'TUSD$', r'USDC$',
                                  r'XRP$', r'USDS$', r'PAX$', r'TRX$', r'BUSD$', r'NGN$',
                                  r'RUB$', r'TRY$', r'EUR$', r'ZAR$', r'BKRW$', r'IDRT$',
                                  r'GBP$', r'UAH$', r'BIDR$', r'AUD$', r'DAI$', r'BRL$',
                                  r'BVND$'}}, value="", regex=True) #in Base Asset deleting of 2 symbols
db3 = db2.replace(to_replace={"Quote Asset":
                                 {r'\w+?<=BTC', r'\w+?<=ETH'}}, value="", regex=True)

print(db3.head())
db3.to_csv('new_db.csv')
# print(db.head())
# print(db.index)
# print(db.dtypes)

