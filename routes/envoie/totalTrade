from pymongo import MongoClient
from datetime import timedelta
from bson import ObjectId

client = MongoClient('mongodb+srv://pierre:ztxiGZypi6BGDMSY@atlascluster.sbpp5xm.mongodb.net/?retryWrites=true&w=majority')
db = client['test']

def totalTrade(data, collection_unitaire):

    print('igoooooo')

    trades = sorted(data, key=lambda x: x['timestamp'])

    print(trades)

    total_trades = len(trades)

    position_number = 1

    for trade in trades:
        trade['totaltrade'] = position_number

        position_number += 1

        #collection_unitaire.update_one({'_id': trade['_id']}, {'$set': trade})

    if total_trades == 0:
        return 0

    last_trade = trades[-1]
    last_trade['totaltrade'] = total_trades
    print(last_trade)
    #collection_unitaire.update_one({'_id': last_trade['_id']}, {'$set': last_trade})
    #collection_unitaire.update_one({}, {'$set': {'totaltrade': last_trade['totaltrade']}}, upsert=True)

    first_trade = trades[0]
    if first_trade:
        print("igo")
        #collection_unitaire.update_one({'_id': first_trade['_id']}, {'$set': {'totaltrade': 1}})
        return 1
    else:
        print('oooo')
        return last_trade['totaltrade']
