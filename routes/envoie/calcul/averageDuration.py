from pymongo import MongoClient
from datetime import datetime, timedelta

client = MongoClient('mongodb+srv://pierre:ztxiGZypi6BGDMSY@atlascluster.sbpp5xm.mongodb.net/?retryWrites=true&w=majority')
db = client['test']

def averageDuration(data, collection_unitaire):

    documents = data
    
    total_duration = timedelta()
    document_count = 0
    
    for doc in documents:
        if 'duration' in doc:
            duration_str = doc['duration']
            duration_parts = duration_str.split(':')
            duration = timedelta(hours=int(duration_parts[0]), minutes=int(duration_parts[1]), seconds=int(duration_parts[2]))
            total_duration += duration
            document_count += 1
 
    average_duration = total_duration / document_count if document_count > 0 else timedelta()
    
    unitaire_collection = db[collection_unitaire]
    unitaire_collection.update_one({}, {'$set': {'average_duration': str(average_duration)}}, upsert=True)

    return average_duration
