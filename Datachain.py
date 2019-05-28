from BigchaindbConnector import BigchaindbConnector

import pandas as pd

class Datachain():

    def __init__(self, backend, endpoints, params=None):
        if backend == 'Bigchaindb':
            try:
                self.connector = BigchaindbConnector(endpoints, params)
                self.keypair = None
            except Exception:
                raise DatachainException(
                    'Datachain>> Failed to CONNECT to Bigchaindb '
                    'with given endpoints: ' + str(endpoints) + ' and params: ' + str(params) + '...'
                )
            else:
                print('Datachain>> Successfully connected to ' + backend + ' with endpoints: ' + str(endpoints) + '...')
        else:
            raise DatachainException('Datachain>> backend: ' + backend + ' is not supported...')

    def getBackendConfig(self):
        return self.connector.getConnectorConfig()

    def generateKeypair(self, append=False):
        try:
            k = self.connector.generateKeypair()
            keys = {'private_key': k.private_key, 'public_key': k.public_key}
            if append:
                self.keypair = keys
        except Exception:
            raise DatachainException('Datachain>> backend could not generate keypair...')
        return keys

    def createDataAsset(self, data, desc=None):
        try:
            a = self.connector.createDataAsset(data, desc)
        except Exception:
            raise DatachainException('Datachain>> Failed to CREATE asset... ' +
                                     'Maybe data provided is not a collection (e.g., dict)...')
        else:
            print('Datachain>> Successfully created asset with data: ' + str(data))
        return a

    # if no private/public keys are given, then appended keypair will be tried.
    def submitAssetCreateTranscation(self, asset, mutable_data, public_key=None, private_key=None):
        if (public_key is None and private_key is None) and self.keypair is None:
            raise DatachainException('Datachain>> No keypair provided...')

        public_key = public_key if public_key else self.keypair['public_key']
        private_key = private_key if private_key else self.keypair['private_key']

        try:
            resp = self.connector.submitAssetCreateTranscation(asset, mutable_data, public_key, private_key)
        except Exception as e:
            raise DatachainException('Datachain>> submitted asset creation transaction FAILED with ...' + e.__str__())
        return resp

    # if no private public keys are given, then appended keypair will be tried.
    # this means that the transfer transaction is just an update of the asset
    # mutable data NOT a change of ownership.
    def submitAssetAppendTranscation(self, asset_id, prev_trans_id, mutable_data,
                                     recipients_public_key=None, owners_private_key=None):
        if (recipients_public_key is None and owners_private_key is None) and self.keypair is None:
            raise DatachainException('Datachain>> No keypair provided...')

        recipients_public_key = recipients_public_key if recipients_public_key else self.keypair['public_key']
        owners_private_key = owners_private_key if owners_private_key else self.keypair['private_key']
        print(recipients_public_key,' ', owners_private_key)
        try:
            resp = self.connector.submitAssetAppendTranscation(asset_id, prev_trans_id, mutable_data,
                                                               recipients_public_key, owners_private_key)
        except Exception as e:
            raise DatachainException('Datachain>> submitted asset append transaction FAILED with ...' + e.__str__())
        return resp

    def getAssetBlockInLedger(self, trans_id, res_type = 'raw'):
        r = self.connector.getAssetBlockInLedger(trans_id)
        if res_type == 'pandas':
            return pd.DataFrame(r)
        return r

    def getAssetTransactions(self, asset_id, latest=False, descending=False, res_type='raw'):
        data = self.connector.getAssetTransactions(asset_id)
        if res_type == 'pandas':
            df = pd.DataFrame(data)
            if latest:
                df = df[-1:]
            if descending:
                df = df.sort_index(ascending=False)
            return df

        if latest:
            data = data[-1: ]
        if descending:
            data = data.reverse()
        return data

    def getAsset(self, asset_id, res_type='raw'):
        data = self.connector.getAsset(asset_id)
        if res_type == 'pandas':
            df = pd.Series(data)
            return df
        return data

    def getAssetMutableData(self, asset_id, latest=False, descending=False, res_type='raw'):
        data = self.connector.getAssetMutableData(asset_id)
        if res_type == 'pandas':
            df = pd.DataFrame(data)
            if latest:
                df = df[-1:]
            if descending:
                df = df.sort_index(ascending=False)
            return df

        if latest:
            data = data[-1:]
        if descending:
            data = data.reverse()
        return data

    def getAssetOwnership(self, asset_id, latest=False, descending=False, res_type='raw'):
        data = self.connector.getAssetOwnership(asset_id)
        if res_type == 'pandas':
            df = pd.DataFrame(data)
            if latest:
                df = df[-1:]
            if descending:
                df = df.sort_index(ascending=False)
            return df

        if latest:
            data = data[-1:]
        if descending:
            data = data.reverse()
        return data


class DatachainException(Exception):
    pass