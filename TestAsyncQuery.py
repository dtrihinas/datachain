from Datachain import Datachain

import pandas as pd
pd.set_option('display.max_colwidth', 100)
pd.set_option('display.max_columns',10)

dc = Datachain('Bigchaindb', ['http://localhost:9984'])
print(dc.getBackendConfig())

assets = [
    ('22ca11ee891a564441c21be96914d3580df66aea9146b985cae0be2b8b460a59'),
    ('38fdf2d368db6af209759dc9d0936a636ca27fa55f0c7e9c5387d4525e3bfebd'),
    ('c97fc993abfcd000e53c140c0b7da68219fa40d78a5d468467f1453bbe89dcd6'),
    ('68222d701e65944d5415e2c4385a5feb009451648f80ce14b54f383e823036a9')
]
res = dc.async_query('getAsset',assets)
for r in res:
    print(r)