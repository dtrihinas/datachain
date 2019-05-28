from BigchaindbConnector import BigchaindbConnector

import pandas as pd
import numpy as np
desired_width=1000
pd.set_option('display.width', desired_width)
np.set_printoptions(linewidth=desired_width)
pd.set_option('display.max_columns',10)

bdb = BigchaindbConnector()
print(str(bdb.getConnectorConfig()))

keys = bdb.generateKeypair(append=True)
print('private key: ' + keys.private_key)
print('public key: ' + keys.public_key)

data = {
    'bicycle_serial_number': 'abcd1234',
    'bicycle_manufacturer': 'bkfab',
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

mdata = {'km': '1000', 'color': 'blue'}
resp = bdb.submitAssetAppendTranscation(aid, resp['trans_id'], mdata)

df = bdb.getAssetTransactions(aid, latest=True)

print(df.columns)
print(df['asset'])
print(df['id'])
print(df['metadata'])

assdf = bdb.getAsset(aid)
print(assdf)

meta = bdb.getAssetMutableData(aid)
print(meta)

bob = bdb.generateKeypair()
print('private key: ' + bob.private_key)
print('public key: ' + bob.public_key)
mdata = {'km': '2500', 'color': 'blue'}
resp = bdb.submitAssetAppendTranscation(aid, resp['trans_id'], mdata, recipient_public_key=bob.public_key)

print(bdb.getAssetTransactions(aid))
print(resp)

kate = bdb.generateKeypair()
print('private key: ' + kate.private_key)
print('public key: ' + kate.public_key)
mdata = {'km': '2750', 'color': 'red'}
resp = bdb.submitAssetAppendTranscation(aid, resp['trans_id'], mdata, recipient_public_key=kate.public_key, owner_private_key=bob.private_key)

print(bdb.getAssetTransactions(aid))
print(resp)

odf = bdb.getAssetOwnership(aid)
print(odf)