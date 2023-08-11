from flask import Flask, Blueprint, jsonify, request
from pymongo import MongoClient

app = Flask(__name__)
daytotal = Blueprint('daytotal', __name__)



client = MongoClient('mongodb+srv://pierre:ztxiGZypi6BGDMSY@atlascluster.sbpp5xm.mongodb.net/test?retryWrites=true&w=majority')
db = client['test']

@daytotal.route('/daytotal', methods=['POST'])  # I changed it to POST for passing username data safely
def calculate_daycount(data):
    data = request.json
    username = data.get('username')
    
    if not username:
        return jsonify({"error": "Username is required!"}), 400

    collection_name = f"{username}_close"
    collection = db[collection_name]
    collection_unit = f"{username}_unitaire"
    unitaire_collection = db[collection_unit]
    

    # Assuming that there's a 'date' field in each document which contains the date
    distinct_dates = collection.aggregate([
        {
            "$group": {
                "_id": "$date"
            }
        },
        {
            "$count": "distinctDateCount"
        }
    ])

    result = list(distinct_dates)
    if result:
        return result[0]['distinctDateCount']
   
    unitaire_collection.update_one({}, {"$set": {"daytotal": distinct_count}}, upsert=True)
    return distinct_count


