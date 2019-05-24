from bigchaindb_driver import BigchainDB
from bigchaindb_driver.crypto import generate_keypair


bdb_endpoint = 'http://localhost:9984'
bdb = BigchainDB(bdb_endpoint)

keypair = generate_keypair()

print('private key: ' + keypair.private_key)
print('public key: ' + keypair.public_key)

#In asset there must be a 'data' property with the data in it.
bicycle = {
            'data': {
                'bicycle': {
                    'serial_number': 'abcd1234',
                    'manufacturer': 'bkfab',
                },
            },
}

#asset data that is mutable
metadata = {'km': '30'}

#prepare asset creation for blockchain transaction
prepared_creation_tx = bdb.transactions.prepare(
    operation = 'CREATE',
    signers = keypair.public_key,
    asset=bicycle,
    metadata = metadata
)

print(prepared_creation_tx)

#The transaction now needs to be fulfilled by signing it with Alice’s private key:
fulfilled_creation_tx = bdb.transactions.fulfill(
    prepared_creation_tx, private_keys = keypair.private_key)

print(fulfilled_creation_tx)

#Sent transaction over to a BigchainDB node:
sent_creation_tx = bdb.transactions.send_commit(fulfilled_creation_tx)

print(sent_creation_tx)

txid = fulfilled_creation_tx['id']
print(txid)