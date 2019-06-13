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
        data = r.json()
        tid = data.get('transactionId') #only transactions have id, not assets
        resp = {
            'data': data,
            'status': r.status_code,
            'transactionId': tid
        }
        return resp

    def submitAssetAppendTransaction(self, asset_id, asset_type, ass_data, prev_trans_id, prev_owner, new_owner):
        url = self.endpoints + asset_type + '/' + asset_id
        r = requests.put(url, ass_data, headers=self.headers)
        data = r.json()
        tid = data.get('transactionId')  # only transactions have id, not assets
        resp = {
            'data': data,
            'status': r.status_code,
            'transactionId': tid
        }
        return resp

    def getAssetBlockInLedger(self, trans_id, trans_type):
        url = self.endpoints + trans_type + '/' + trans_id
        r = requests.get(url, headers=self.headers)
        if r.status_code == 200:
            return r.json()
        return None

    def getAssetTransactions(self, asset_id, asset_type,  trans_type):
        asset = self.getAsset(asset_id, asset_type)
        print(asset)
        if asset is None:
            return None
        field_id = ''
        for k,v in asset.items():
            if v == asset_id:
                field_id = k
        url = self.endpoints + trans_type
        params = dict()
        params['filter'] = '{"' + field_id + '":"' + asset_id + '"}'

        r = requests.get(url, headers=self.headers, params=params)
        if r.status_code == 200:
            return r.json()

    def getAsset(self, asset_id, asset_type):
        url = self.endpoints + asset_type + '/' + asset_id
        r = requests.get(url, headers=self.headers)
        if r.status_code == 200:
            return r.json()
        return None

    def getAssetMutableData(self, asset_id, asset_type):
        # not applicable for hyperledger
        # assets can be altered by owner through new transaction
        pass

    def getAssetOwnership(self, asset_id, asset_type):
        pass