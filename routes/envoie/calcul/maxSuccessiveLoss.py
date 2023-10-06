from pymongo import MongoClient

client = MongoClient('mongodb+srv://pierre:ztxiGZypi6BGDMSY@atlascluster.sbpp5xm.mongodb.net/?retryWrites=true&w=majority')
db = client['test']

def maxSuccessiveLoss(data, collection_unitaire):

    max_successive_losses_count = 0
    current_successive_losses_count = 0
    #previous_identifier = None

    for doc in data:
        profit = doc['profit']

        if profit < 0:
            current_successive_losses_count += 1
        else:
            if current_successive_losses_count > max_successive_losses_count:
                max_successive_losses_count = current_successive_losses_count
            current_successive_losses_count = 0

    if current_successive_losses_count > max_successive_losses_count:
        max_successive_losses_count = current_successive_losses_count

    unitaire_collection = db[collection_unitaire]
    unitaire_collection.update_one({}, {'$set': {'max_successive_loss': max_successive_losses_count}}, upsert=True)

    return max_successive_losses_count
