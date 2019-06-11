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

        #perform simple status request to see if endpoint up and running
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

    def createParticipant(self, participant, participant_type):
        url = self.endpoints + participant_type
        r = requests.post(url, participant, headers=self.headers)

        resp = {
            'data': r.json(),
            'status': r.status_code
        }

        return resp


    def updateParticipant(self, participant, participant_type):
        url = self.endpoints + participant_type
        r = requests.put(url, participant, headers=self.headers)

        resp = {
            'data': r.json(),
            'status': r.status_code
        }

        return resp

    def submitAssetCreateTransaction(self, asset, asset_type, ass_data, owner):
        url = self.endpoints + asset_type
        r = requests.post(url, asset, headers=self.headers)

        resp = {
            'data': r.json(),
            'status': r.status_code
        }

        return resp

    def submitAssetAppendTransaction(self, asset_id, asset_type, ass_data, prev_trans_id, prev_owner, new_owner):
        url = self.endpoints + asset_type + '/' + asset_id
        r = requests.put(url, ass_data, headers=self.headers)

        resp = {
            'data': r.json(),
            'status': r.status_code
        }

        return resp

    def getAssetBlockInLedger(self, trans_id):
        pass

    def getAssetTransactions(self, asset_id, limit=-1):
        pass

    def getAsset(self, asset_id, asset_type):
        url = self.endpoints + asset_type + '/' + asset_id
        r = requests.get(url, headers=self.headers)

        resp = {
            'data': r.json(),
            'status': r.status_code
        }

        return resp

    def getAssetMutableData(self, asset_id, limit=-1):
        pass

    def getAssetOwnership(self, asset_id, limit=-1):
        pass