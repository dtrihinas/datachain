
class BlockchainConnector:

    def __init__(self, backend, endpoints):
        self.backend = backend
        self.endpoints = endpoints

    def getConnectorConfig(self):
        pass

    def createParticipant(self, participant, participant_type):
        pass

    def updateParticipant(self, participant, participant_type):
        pass

    def submitAssetCreateTransaction(self, asset, asset_type, ass_data, owner):
        pass

    def submitAssetAppendTransaction(self, asset_id, asset_type, ass_data, prev_trans_id, prev_owner, new_owner):
        pass

    def getAssetBlockInLedger(self, trans_id, trans_type):
        pass

    def getAssetTransactions(self, asset_id, asset_type,  trans_type):
        pass

    def getAsset(self, asset_id, asset_type):
        pass

    def getAssetMutableData(self, asset_id, asset_type):
        pass

    def getAssetOwnership(self, asset_id, asset_type):
        pass

class BlockchainConnectorException(Exception):
    pass
