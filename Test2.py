from Datachain import Datachain

import pandas as pd
pd.set_option('display.max_colwidth', 100)
pd.set_option('display.max_columns',10)

dc = Datachain('Hyperledger', ['http://localhost:3000'], {'x-api-key': '1234'})
print(dc.getBackendConfig())

asset = {
    "$class": "org.example.trading.Commodity",
    "tradingSymbol": "BBB",
    "description": "something!",
    "mainExchange": "NASDAQ",
    "quantity": 1,
    "owner": "resource:org.example.trading.Trader#Trader2"
}

resp = dc.submitAssetCreateTransaction(asset, asset_type='Commodity')
print(resp)

asset["quantity"] = 5

resp = dc.submitAssetAppendTransaction('BBB', asset_type='Commodity', mutable_data=asset)
print(resp)