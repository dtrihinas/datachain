
class BlockchainConnector:

    def __init__(self, backend, endpoints):
        self.backend = backend
        self.endpoints = endpoints

    def getConnectorConfig(self):
        pass

    def createParticipant(self, participant):
        pass

    def updateParticipant(self, participant):
        pass

    def submitAssetCreateTransaction(self, asset, asset_type, ass_data, owner):
        pass

    def submitAssetAppendTransaction(self, asset_id, asset_type, ass_data, prev_trans_id, prev_owner, new_owner):
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
