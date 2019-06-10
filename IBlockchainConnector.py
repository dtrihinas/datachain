
class BlockchainConnector:

    def __init__(self, backend, endpoints):
        self.backend = backend
        self.endpoints = endpoints
        self.keypair = None

    def getConnectorConfig(self):
        pass

    def generateKeypair(self):
        pass

    def createDataAsset(self, data, desc):
        pass

    def submitAssetCreateTransaction(self, asset, asset_type, mutable_data, public_key, private_key):
        pass

    def submitAssetAppendTransaction(self, asset_id, asset_type, prev_trans_id, mutable_data, recipients_public_key, owners_private_key):
        pass

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

class BlockchainConnectorException(Exception):
    pass
