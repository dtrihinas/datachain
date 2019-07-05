from Datachain import Datachain

import pandas as pd
pd.set_option('display.max_colwidth', 100)
pd.set_option('display.max_columns',10)

dc = Datachain('Hyperledger', ['http://localhost:3000'], {'x-api-key': '1234'})
print(dc.getBackendConfig())

traders = []

trader = {
 "$class": "org.example.trading.Trader",
 "tradeId": "T0001",
 "firstName": "John",
 "lastName": "Smith"
}
traders.append(trader)

trader = {
    "$class": "org.example.trading.Trader",
    "tradeId": "T0002",
    "firstName": "Maria",
    "lastName": "Garcia"
}
traders.append(trader)

trader = {
    "$class": "org.example.trading.Trader",
    "tradeId": "T0003",
    "firstName": "Gianna",
    "lastName": "Halini"
}
traders.append(trader)


trader = {
    "$class": "org.example.trading.Trader",
    "tradeId": "T0004",
    "firstName": "James",
    "lastName": "Anders"
}
traders.append(trader)


resp = dc.createParticipant(traders[0], participant_type='Trader', save=True)
print(resp)

for i in range(1,4):
    resp = dc.createParticipant(traders[i], participant_type='Trader')
    print(resp)

assets = []
asset = {
    "$class": "org.example.trading.Commodity",
    "tradingSymbol": "AAA",
    "description": "An awesome asset!",
    "mainExchange": "NASDAQ",
    "quantity": 10,
    "owner": "resource:org.example.trading.Trader#T0001"
}
assets.append(asset)

asset = {
    "$class": "org.example.trading.Commodity",
    "tradingSymbol": "XYZ",
    "description": "Something valuable",
    "mainExchange": "NASDAQ",
    "quantity": 500,
    "owner": "resource:org.example.trading.Trader#T0002"
}
assets.append(asset)

asset = {
    "$class": "org.example.trading.Commodity",
    "tradingSymbol": "XMG",
    "description": "Everyday commodity",
    "mainExchange": "LSE",
    "quantity": 2,
    "owner": "resource:org.example.trading.Trader#T0001"
}
assets.append(asset)

asset = {
    "$class": "org.example.trading.Commodity",
    "tradingSymbol": "BEF",
    "description": "some desc for asset",
    "mainExchange": "DAX",
    "quantity": 21,
    "owner": "resource:org.example.trading.Trader#T0003"
}
assets.append(asset)

asset = {
    "$class": "org.example.trading.Commodity",
    "tradingSymbol": "MES",
    "description": "some desc for asset",
    "mainExchange": "CAC",
    "quantity": 28,
    "owner": "resource:org.example.trading.Trader#T0004"
}
assets.append(asset)

asset = {
    "$class": "org.example.trading.Commodity",
    "tradingSymbol": "YYE",
    "description": "some desc for asset",
    "mainExchange": "DAX",
    "quantity": 35,
    "owner": "resource:org.example.trading.Trader#T0002"
}
assets.append(asset)

asset = {
    "$class": "org.example.trading.Commodity",
    "tradingSymbol": "NAD",
    "description": "some desc for asset",
    "mainExchange": "NASDAQ",
    "quantity": 58,
    "owner": "resource:org.example.trading.Trader#T0001"
}
assets.append(asset)

asset = {
    "$class": "org.example.trading.Commodity",
    "tradingSymbol": "KHS",
    "description": "some desc for asset",
    "mainExchange": "CAC",
    "quantity": 19,
    "owner": "resource:org.example.trading.Trader#T0004"
}
assets.append(asset)

asset = {
    "$class": "org.example.trading.Commodity",
    "tradingSymbol": "RWS",
    "description": "some desc for asset",
    "mainExchange": "LSE",
    "quantity": 8,
    "owner": "resource:org.example.trading.Trader#T0001"
}
assets.append(asset)

asset = {
    "$class": "org.example.trading.Commodity",
    "tradingSymbol": "POW",
    "description": "some desc for asset",
    "mainExchange": "LSE",
    "quantity": 30,
    "owner": "resource:org.example.trading.Trader#T0004"
}
assets.append(asset)


for i in range(10):
    resp = dc.submitAssetCreateTransaction(assets[i], asset_type='Commodity')
    print(resp)

assetAAA = dc.getAsset('AAA', asset_type='Commodity')
print(assetAAA)
assetAAA["quantity"] = 15
print(assetAAA)
resp = dc.submitAssetAppendTransaction('AAA', asset_type='Commodity', ass_data=assetAAA)
print(resp)

asset = {
    "$class": "org.example.trading.Commodity",
     "tradingSymbol": "TRE",
     "description": "some desc for asset",
     "mainExchange": "EUS",
     "quantity": 96,
     "owner": "resource:org.example.trading.Trader#T0002"
}

resp = dc.submitAssetCreateTransaction(asset, asset_type='Commodity')
print(resp)

trade ={
  "$class": "org.example.trading.Trade",
  "commodity": 'AAA',
  "newOwner": 'T0001'
}

resp = dc.submitAssetCreateTransaction(trade, asset_type='Trade')
print(resp)

tid = resp['transactionId']
resp = dc.getAssetBlockInLedger(tid, trans_type='Trade')
print(resp)

resp = dc.getAssetTransactions('AAA', asset_type='Commodity', trans_type='Trade', res_type='pandas')
print(resp)
