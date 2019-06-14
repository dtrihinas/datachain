#Datachain

Datachain is a flexible, lightweight and customizable python library for interoperable access of data from underlying blockchains.

## Datachain Model
Datachain adopts a [CRAB](https://tutorials.bigchaindb.com/crab/) (Create-Retrieve-Append-Burn) approach from data management, which is inherent to the basic 
blockchain principles.

The Datachain model provides CRAB operations for the following:

- Participants
- Assets with immutable and associated data. Multiple asset types as well.
- Transactions... multiple transaction types as well.

## Datachain Data Formatting
Data extracted from underlying blockchains can be retrieved as:

- In `raw` format, meaning exactly as returned from the underlying blockchain.
- In `xml` format.
- In `json` format.
- As a `collection`. Depending on the request this may be a dictionary, list or tuple.
- As a `pandas.Series` for 1d or `pandas.DataFrame` for 2d data. By simply requesting `pandas` the default response is 
a DataFrame.

## Supported Blockchains
Currently, Datachain provides under-the-hood connectors for:

- BigchainDB apps
- Hyperledger Composer apps

## Prerequisites
Datachain requires a python3 version (tested on v3.7.x). Other required libraries are: numpy, pandas, and dicttoxml.

To use the BigchainDB connector, the bigchaindb_driver is required.

