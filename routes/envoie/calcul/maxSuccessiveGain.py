from pymongo import MongoClient

client = MongoClient('mongodb+srv://pierre:ztxiGZypi6BGDMSY@atlascluster.sbpp5xm.mongodb.net/?retryWrites=true&w=majority')
db = client['test']

def maxSuccessiveGain(data, collection_unitaire):

    max_successive_gains_count = 0
    current_successive_gains_count = 0

    for doc in data:
        profit = doc.get('profit', 0)

        if profit > 0:
            current_successive_gains_count += 1
        else:
            if current_successive_gains_count > max_successive_gains_count:
                max_successive_gains_count = current_successive_gains_count
            current_successive_gains_count = 0

    if current_successive_gains_count > max_successive_gains_count:
        max_successive_gains_count = current_successive_gains_count

    unitaire_collection = db[collection_unitaire]
    unitaire_collection.update_one({}, {'$set': {'max_successive_gain': max_successive_gains_count}}, upsert=True)

    return max_successive_gains_count
