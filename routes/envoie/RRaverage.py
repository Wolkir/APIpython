from pymongo import MongoClient

client = MongoClient('mongodb+srv://pierre:ztxiGZypi6BGDMSY@atlascluster.sbpp5xm.mongodb.net/test?retryWrites=true&w=majority')
db = client['test']

def RRaverage(data, collection_unitaire):

    rr_values = []
    for document in data:
        if "RR" in document:
            rr_values.append(document["RR"])

    print("Valeurs de RR dans la collection 'things':", rr_values)

    rr_total = sum(rr_values)
    rr_count = len(rr_values)
    average_rr = rr_total / rr_count if rr_count > 0 else 0

    unitaire_collection = db[collection_unitaire]
    unitaire_collection.update_one({}, {"$set": {"RRaverage": average_rr}}, upsert=True)

    return average_rr
