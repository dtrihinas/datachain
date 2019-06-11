from Datachain import Datachain

import pandas as pd
pd.set_option('display.max_colwidth', 100)
pd.set_option('display.max_columns',10)

dc = Datachain('Bigchaindb', ['http://localhost:9984'])
print(dc.getBackendConfig())

alice = dc.createParticipant(save=True)
print('alice private key: ' + alice['private_key'])
print('alice public key: ' + alice['public_key'])

asset = {
    'bike_serial_number': 'abcd1234',
    'bike_manufacturer': 'bkfab',
    'bike_height_in_cm': 85,
}

#asset data that is mutable
mdata = {'km': '0'}

resp = dc.submitAssetCreateTransaction(asset, ass_data=mdata)
print(resp)

print(dc.getAssetBlockInLedger(resp['trans_id']))
print(dc.getAssetBlockInLedger(resp['trans_id'], res_type='pandas'))

mdata = {'km': '30'}
aid = resp['asset_id']
resp = dc.submitAssetAppendTransaction(aid, ass_data=mdata, prev_trans_id=resp['trans_id'])

mdata = {'km': '1000', 'color': 'blue'}
resp = dc.submitAssetAppendTransaction(aid, ass_data=mdata, prev_trans_id=resp['trans_id'])

s1 = dc.getAssetTransactions(aid, res_type='pandas', latest=True)
s2 = dc.getAssetTransactions(aid, res_type='collection', latest=True)
print(s1.columns)
print(s1['id'])
print(s2[0]['id']) # must be the same with above


a1 = dc.getAsset(aid, res_type='pandas')
a2 = dc.getAsset(aid)
print(a1)
print(a2)

m1 = dc.getAssetMutableData(aid, res_type='pandas')
m2 = dc.getAssetMutableData(aid)
print(m1)
print(m2)


bob = dc.createParticipant()
print('bob private key: ' + bob['private_key'])
print('bob public key: ' + bob['public_key'])

mdata = {'km': '2500', 'color': 'blue'}
resp = dc.submitAssetAppendTransaction(aid, ass_data=mdata, prev_trans_id=resp['trans_id'],
                                       new_owner=bob, prev_owner=alice)

print(dc.getAssetTransactions(aid, res_type='pandas'))
print(resp)

kate = dc.createParticipant()
print('private key: ' + kate['private_key'])
print('public key: ' + kate['public_key'])

mdata = {'km': '2750', 'color': 'red'}

resp = dc.submitAssetAppendTransaction(aid, ass_data=mdata, prev_trans_id=resp['trans_id'],
                                       new_owner=kate, prev_owner=bob)

print(dc.getAssetTransactions(aid))
print(resp)

odf = dc.getAssetOwnership(aid, res_type='pandas')
print(odf)