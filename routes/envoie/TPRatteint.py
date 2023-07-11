from flask import Blueprint, jsonify, request
from pymongo import MongoClient
from datetime import datetime, timedelta
from pymongo.errors import PyMongoError
from bson import ObjectId

import json
import atexit

client = MongoClient('mongodb+srv://pierre:ztxiGZypi6BGDMSY@atlascluster.sbpp5xm.mongodb.net/?retryWrites=true&w=majority')
TPRatteint = Blueprint('TPRatteint', __name__)

def json_serial(obj):
    """Serialize BSON ObjectId and datetime to string."""
    if isinstance(obj, ObjectId):
        return str(obj)
    if isinstance(obj, datetime):
        return obj.isoformat()
    raise TypeError("Type not serializable")

def close_mongo_client():
    try:
        client.close()
    except Exception as e:
        print("An error occurred while closing the MongoDB client:", str(e))

atexit.register(close_mongo_client)

@TPRatteint.route('/TPRatteint', methods=['GET'])
def update_TPRatteint():
    argumentDate = request.args.get('date')
    argumentFiltre = request.args.get('filtre')
    debutDate = request.args.get('debutDate', None)
    finDate = request.args.get('finDate', None)
    db = client['test']
    collection = db['thingsTest']

    if argumentDate == "aujourd'hui":
        date = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
        start_date = date
        end_date = date + timedelta(days=1)
    elif argumentDate == "semaineEnCours":
        date = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
        start_date = date - timedelta(days=date.weekday())
        end_date = start_date + timedelta(days=7)
    elif argumentDate == "semaineGlissante":
        date = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
        start_date = date - timedelta(days=date.weekday() - 1)
        end_date = start_date + timedelta(days=8)
    elif argumentDate == "moisEnCours":
        date = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
        start_date = date.replace(day=1)
        end_date = start_date.replace(month=start_date.month + 1)
    elif argumentDate == "moisGlissant":
        date = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
        start_date = date.replace(day=1) - timedelta(days=1)
        end_date = start_date.replace(month=start_date.month + 1)
    elif debutDate is not None and finDate is not None and argumentDate == "choixLibre":
        start_date = datetime.fromisoformat(debutDate)
        end_date = datetime.fromisoformat(finDate)
    else:
        return jsonify({'message': 'Invalid argument'})

    try:
        query = {
            '$and': [
                {'dateAndTimeOpening': {'$gte': start_date, '$lt': end_date}},
                {'TPR': True},
                {'symbole': argumentFiltre}
            ]
        }
        data = list(collection.find(query))
        data = json.loads(json.dumps(data, default=json_serial))

        return jsonify({'data': data})
    except PyMongoError as e:
        print("An error occurred:", str(e))
        return jsonify({'message': 'Error occurred'})