from BigchaindbConnector import BigchaindbConnector

bdb = BigchaindbConnector()
print(str(bdb.getConnectorConfig()))

keys = bdb.generateKeypair()
print('private key: ' + keys.private_key)
print('public key: ' + keys.public_key)

data = {
    'bicycle': {
        'serial_number': 'abcd1234',
        'manufacturer': 'bkfab',
    }
}

asset = bdb.createDataAsset(data)

#asset data that is mutable
mdata = {'km': '0'}

resp = bdb.submitAssetCreateTranscation(asset, mdata)
print(resp)

mdata = {'km': '30'}

print(bdb.getAssetBlockInLedger(resp['trans_id']))

aid = resp['asset_id']
resp = bdb.submitAssetAppendTranscation(aid, resp['trans_id'], mdata)

mdata = {'km': '1000'}
bdb.submitAssetAppendTranscation(aid, resp['trans_id'], mdata)

dataa = bdb.getAssetTransactions(aid)

for d in dataa:
    print(d)