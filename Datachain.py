from BigchaindbConnector import BigchaindbConnector
from HyperledgerConnector import HyperledgerConnector

from dicttoxml import dicttoxml
import json

import pandas as pd

import asyncio
from concurrent.futures import ThreadPoolExecutor


class Datachain():

    def __init__(self, backend, endpoints, params=None):
        self.saved_participant = None

        try: #connect to backend
            if backend == 'Bigchaindb':
                self.connector = BigchaindbConnector(endpoints, params)
            elif backend == 'Hyperledger':
                self.connector = HyperledgerConnector(endpoints, params)
        except Exception:
            raise DatachainException(
                'Datachain>> Failed to CONNECT to ' + backend +
                'with given endpoints: ' + str(endpoints) + ' and params: ' + str(params) + '...'
            )
        else:
            print('Datachain>> Successfully connected to ' + backend + '...')

    def getBackendConfig(self):
        return self.connector.getConnectorConfig()

    def createParticipant(self, participant=None, participant_type=None, save=False):
        try:
            p = self.connector.createParticipant(participant, participant_type)
            if save:
                self.saved_participant = p
        except Exception:
            raise DatachainException('Datachain>> backend could not generate blockchain participant...')
        return p

    def updParticipant(self, participant, participant_type=None, save=False):
        try:
            p = self.connector.updateParticipant(participant, participant_type)
            if save:
                self.saved_participant = p
        except Exception:
            raise DatachainException('Datachain>> backend could not update blockchain participant...')
        return p


    def submitAssetCreateTransaction(self, asset, asset_type=None, ass_data=None, owner=None):
        if owner is None and self.saved_participant is None:
            raise DatachainException('Datachain>> No participant previously saved or provided...')
        if owner is None:
            owner = self.saved_participant
        resp = None
        try:
            resp = self.connector.submitAssetCreateTransaction(asset, asset_type, ass_data, owner)
        except Exception as e:
            raise DatachainException('Datachain>> submitted asset CREATE transaction FAILED with ...' + e.__str__())
        return resp


    def submitAssetAppendTransaction(self, asset_id, asset_type=None,  ass_data=None, prev_trans_id=None,
                                     prev_owner=None, new_owner=None):
        if (prev_owner is None and new_owner is None) and self.saved_participant is None:
            raise DatachainException('Datachain>> No participant previously saved or provided...')

        if prev_owner is None and new_owner is None:
            prev_owner = self.saved_participant
            new_owner = self.saved_participant

        try:
            resp = self.connector.submitAssetAppendTransaction(asset_id, asset_type, ass_data, prev_trans_id,
                                                               prev_owner, new_owner)
        except Exception as e:
            raise DatachainException('Datachain>> submitted asset APPEND transaction FAILED with ...' + e.__str__())
        return resp

    def getAssetBlockInLedger(self, trans_id, trans_type= None, res_type = 'raw'):
        r = self.connector.getAssetBlockInLedger(trans_id, trans_type)
        return r if res_type == 'raw' else self._format_response(r, res_type)

    def getAssetTransactions(self, asset_id, asset_type=None, trans_type=None,
                             latest=False, sorting=False, res_type='raw'):
        data = self.connector.getAssetTransactions(asset_id, asset_type, trans_type)
        return data if res_type == 'raw' else self._format_response(data, res_type, latest, sorting)

    def getAsset(self, asset_id, asset_type=None, res_type='raw'):
        data = self.connector.getAsset(asset_id, asset_type)
        if res_type == 'pandas':
            res_type = 'pandas.Series'
        return data if res_type == 'raw' else self._format_response(data, res_type)

    def getAssetMutableData(self, asset_id, asset_type=None, latest=False, sorting=False, res_type='raw'):
        data = self.connector.getAssetMutableData(asset_id, asset_type)
        return data if res_type == 'raw' else self._format_response(data, res_type, latest, sorting)

    def getAssetOwnership(self, asset_id, asset_type=None, latest=False, sorting=False, res_type='raw'):
        data = self.connector.getAssetOwnership(asset_id, asset_type)
        return data if res_type == 'raw' else self._format_response(data, res_type, latest, sorting)

    def _format_response(self, res, res_type, latest=False, sorting=False):
        # fix below hack to check for collections
        if not isinstance(res, (dict, list)):
            raise DatachainException('Datachain>> Response must be a collection to be further formated...')

        if 'pandas' in res_type:
            r = None
            if res_type == 'pandas.Series':
                r = pd.Series(res)
            else:
                r = pd.DataFrame(res)
            if latest:
                r = r[-1:]
            if sorting:
                r = r.sort_index(ascending=False) #sorting in descending order for recent events first
            return r

        # collection
        if latest:
            res = res[-1:]
        if sorting:
            res.reverse()

        if res_type == 'xml':
            return dicttoxml(res, root=False, attr_type=False)

        if res_type == 'json':
            return json.dumps(res)

        return res

    def async_query(self, func, params_per_task=None):
        try:
            query = getattr(self, func) #convert func name to actual function
            loop = asyncio.get_event_loop()
            future = asyncio.ensure_future(self._getDataAsync(query, params_per_task))
            loop.run_until_complete(future)
            return future.result()
        except AttributeError:
            raise DatachainException('Datachain>> requested query' + func + ' not available...')

    async def _getDataAsync(self, func, params_per_task):
        responses = []
        #TODO allow users to define max workers and have as default max cpu core count
        with ThreadPoolExecutor(max_workers=10) as executor:
            loop = asyncio.get_event_loop()
            tasks = [
                loop.run_in_executor(executor, func, params)
                for params in params_per_task
            ]
            for resp in await asyncio.gather(*tasks):
                responses.append(resp)
        return responses

    def somefunc(self, param1):
        return str(param1)

class DatachainException(Exception):
    pass