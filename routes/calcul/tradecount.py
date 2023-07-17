
from flask import Flask, Blueprint, jsonify
from pymongo import MongoClient

tradecount = Blueprint('tradecount', __name__)

@tradecount.route('/tradecount', methods=['GET'])
def calculate_tradecount():
    client = MongoClient('mongodb+srv://pierre:ztxiGZypi6BGDMSY@atlascluster.sbpp5xm.mongodb.net/?retryWrites=true&w=majority')
    db = client['test']
    collection = db['things']

    pipeline = [
        {
            "$group": {
                "_id": {
                    "$dateToString": { "format": "%Y-%m-%d", "date": { "$toDate": "$dateAndTimeOpening" } }
                },
                "count": { "$sum": 1 }
            }
        },
        {
            "$group": {
                "_id": None,
                "average_count": { "$avg": "$count" }
            }
        }
    ]

    result = list(collection.aggregate(pipeline))

    average_count = result[0]["average_count"]

 

    print(f"Average count: {average_count}")
    unitaire_collection = db['unitaire']
  

    unitaire_collection.update_one({}, {"$set": {"tradecount": average_count}}, upsert=True)
    return jsonify({"average_count": average_count})