from pymongo import MongoClient

client = MongoClient('mongodb+srv://pierre:ztxiGZypi6BGDMSY@atlascluster.sbpp5xm.mongodb.net/?retryWrites=true&w=majority')
db = client['test']

def maxProfit(data, collection_unitaire):

    max_profit = max((d for d in data if d.get("profit", 0) > 0), key=lambda x: x["profit"])

    if max_profit:
        profit_value = max_profit['profit']
        
        unitaire_collection = db[collection_unitaire]
        unitaire_collection.update_one({}, {'$set': {'Max profit': (profit_value)}}, upsert=True)

    return profit_value
