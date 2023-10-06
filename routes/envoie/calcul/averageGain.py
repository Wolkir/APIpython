from pymongo import MongoClient

client = MongoClient('mongodb+srv://pierre:ztxiGZypi6BGDMSY@atlascluster.sbpp5xm.mongodb.net/?retryWrites=true&w=majority')
db = client['test']

def averageGain(data, collection_unitaire):
  
    positive_gains_total = 0
    positive_gains_count = 0
    positive_ticket_numbers = set()

    for doc in data:
        profit = doc['profit']
        ticket_number = doc['ticketNumber']
        
        if profit > 0 and ticket_number not in positive_ticket_numbers:
            positive_gains_total += profit
            positive_gains_count += 1
            positive_ticket_numbers.add(ticket_number)

    average_gain = positive_gains_total / positive_gains_count if positive_gains_count > 0 else 0

    unitaire_collection = db[collection_unitaire]
    unitaire_collection.update_one({}, {'$set': {'averagegain': (average_gain)}}, upsert=True)

    return average_gain
