from IBlockchainConnector import BlockchainConnector
from IBlockchainConnector import BlockchainConnectorException

from bigchaindb_driver import BigchainDB
from bigchaindb_driver.crypto import generate_keypair

import pandas as pd

class BigchaindbConnector(BlockchainConnector):

    # Bigchaindb requires list of endpoints given as full urls and
    # optional dictionary of parameters called headers (e.g., app_id)
    def __init__(self, endpoints = ['http://localhost:9984'], params = None):
        BlockchainConnector.__init__(self, 'Bigchaindb', endpoints)
        self.headers = params
        self.conn = BigchainDB(*self.endpoints, headers = self.headers)
        self.conn.info() #if this fails exception generated

    def getConnectorConfig(self):
        config = dict()
        config['backend'] = self.backend
        config['endpoints'] = self.endpoints
        config['params'] = self.headers
        return config

    def generateKeypair(self):
        return generate_keypair()

    def createDataAsset(self, data, desc = None):
        asset = dict()
        # In asset there must be a 'data' property with the data in it.
        asset['data'] = data
        if desc:
            asset['description'] = desc
        return asset

    def submitAssetCreateTranscation(self, asset, mutable_data, public_key, private_key):
        # prepare asset creation for blockchain transaction
        prepared_create_tx = self.conn.transactions.prepare(
            operation = 'CREATE',
            signers = public_key if public_key else self.keypair.public_key,
            asset = asset,
            metadata = mutable_data
        )

        # The transaction now needs to be fulfilled by signing it with the private key:
        fulfilled_create_tx = self.conn.transactions.fulfill(
            prepared_create_tx,
            private_keys=private_key if private_key else self.keypair.private_key
        )

        print('BigChainConnector>> Asset prepared, signed and verified for submission')

        # Send transaction over to a BigchainDB node
        # Commit (opposed to async) waits until the transaction is committed to a block or a timeout is reached.
        self.conn.transactions.send_commit(fulfilled_create_tx)

        txid = fulfilled_create_tx['id']
        print('BigChainConnector>> Asset committed to blockchain ledger with transaction id: ' + txid)

        resp = {
            'asset_id': txid, #CREATE ops have same asset and trans id
            'trans_id': txid,
            'success': True
        }
        return resp

    def submitAssetAppendTranscation(self, asset_id, prev_trans_id, mutable_data, recipients_public_key, owners_private_key):
        prev_trans = self.conn.transactions.retrieve(prev_trans_id)
        if not prev_trans:
            return

        transfer_asset = {
            'id': asset_id
        }

        output_index = 0
        output = prev_trans['outputs'][output_index]

        transfer_input = {
            'fulfillment': output['condition']['details'],
            'fulfills': {
                'output_index': output_index,
                'transaction_id': prev_trans['id'],
            },
            'owners_before': output['public_keys'],
        }

        prepared_transfer_tx = self.conn.transactions.prepare(
            operation = 'TRANSFER',
            asset = transfer_asset,
            inputs = transfer_input,
            recipients = recipients_public_key,
            metadata = mutable_data
        )

        fulfilled_transfer_tx = self.conn.transactions.fulfill(
            prepared_transfer_tx,
            private_keys = owners_private_key,
        )

        print('BigChainConnector>> Asset prepared, signed and verified for submission')

        self.conn.transactions.send_commit(fulfilled_transfer_tx)

        txid = fulfilled_transfer_tx['id']
        print('BigChainConnector>> Asset transfer committed to blockchain ledger with transaction id: ' + txid)

        resp = {
            'asset_id': asset_id,
            'trans_id': txid,
            'success': True
        }
        return resp

    def getAssetBlockInLedger(self, trans_id):
        # if block_height is None then either trans does not exist,
        # invalid or simply queued - so not processed yet.
        block_height = self.conn.blocks.get(txid=trans_id)
        if block_height:
            return self.conn.blocks.retrieve(str(block_height))
        return None

    def getAssetTransactions(self, asset_id, limit=-1):
        #limit not supported
        return self.conn.transactions.get(asset_id = asset_id)


    def getAsset(self, asset_id):
        data = self.conn.transactions.get(asset_id = asset_id, operation = 'CREATE')
        return data[0]['asset']['data']

    def getAssetMutableData(self, asset_id, limit=-1):
        #limit not supported
        data = self.conn.transactions.get(asset_id = asset_id)
        ml = []
        for m in data:
            ml.append(m['metadata'])
        return ml

    def getAssetOwnership(self, asset_id):
        #limit not supported
        data = self.conn.transactions.get(asset_id=asset_id)
        ml = []
        for m in data:
            obj = dict()
            obj['trans_id'] = m['id']
            obj['operation'] = m['operation']
            obj['owners_before'] = m['inputs'][0]['owners_before']
            obj['current_owners'] = m['outputs'][0]['public_keys']
            ml.append(obj)
        return ml