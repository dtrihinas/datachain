
class BlockchainConnector:

    def __init__(self, backend, endpoints):
        self.backend = backend
        self.endpoints = endpoints
        self.keypair = None

    def getConnectorConfig(self):
        pass

    def generateKeypair(self, append = True):
        pass

    def createDataAsset(self):
        pass

    def submitAssetCreateTranscation(self, asset, mutable_data, public_key=None, private_key=None):
        pass

    def submitAssetAppendTranscation(self, asset_id, prev_trans_id, mutable_data = None, recipient_public_key = None, owner_private_key = None):
        pass

    def getAssetBlockInLedger(self, trans_id):
        pass

    def getAssetTransactions(self, asset_id):
        pass



class BlockchainConnectorException(Exception):
    pass
