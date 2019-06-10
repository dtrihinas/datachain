from IBlockchainConnector import BlockchainConnector, BlockchainConnectorException

import requests

class HyperledgerConnector(BlockchainConnector):

    def __init__(self, endpoints = ['http://localhost:3000'], params = None):
        BlockchainConnector.__init__(self, 'Hyperledger', endpoints)
        self.endpoints = endpoints[0]
        self.headers = dict()

        if params and isinstance(params, dict):
            try:
                self.headers['x-api-key'] = params['x-api-key']
            except Exception:
                raise BlockchainConnectorException('HyperledgerConnector>> params must be a dictionary collection with valid params...')

        r = requests.get(self.endpoints, headers=self.headers)

        if r.status_code == 200:
            self.endpoints += '/api/'
        else:
            raise BlockchainConnectorException('HyperledgerConnector>> Failed to connect to ' + self.endpoints + '...')

    def getConnectorConfig(self):
        config = dict()
        config['backend'] = self.backend
        config['endpoints'] = self.endpoints
        config['params'] = self.headers
        return config

    def generateKeypair(self):
        pass

    def createDataAsset(self, data, desc):
        #nothing to prepare for hyperledger
        pass

    def submitAssetCreateTransaction(self, asset, asset_type, mutable_data, public_key, private_key):
        url = self.endpoints + asset_type
        r = requests.post(url, asset, headers=self.headers)

        resp = {
            'data': r.json(),
            'status': r.status_code
        }

        return resp

    def submitAssetAppendTransaction(self, asset_id, asset_type, prev_trans_id, mutable_data, recipients_public_key,
                                     owners_private_key):
        url = self.endpoints + asset_type + '/' + asset_id
        r = requests.put(url, mutable_data, headers=self.headers)

        resp = {
            'data': r.json(),
            'status': r.status_code
        }

        return resp

    def getAssetBlockInLedger(self, trans_id):
        pass

    def getAssetTransactions(self, asset_id, limit=-1):
        pass

    def getAsset(self, asset_id):
        pass

    def getAssetMutableData(self, asset_id, limit=-1):
        pass

    def getAssetOwnership(self, asset_id, limit=-1):
        pass