from flask import Flask, Blueprint, request, jsonify, current_app
from pymongo import MongoClient
import json
from bson import ObjectId

def json_serial(obj):
    if isinstance(obj, ObjectId):
        return str(obj)
    raise TypeError("Type non sérialisable")

app = Flask(__name__)

app.config['MONGO_URI'] = 'mongodb+srv://pierre:ztxiGZypi6BGDMSY@atlascluster.sbpp5xm.mongodb.net/?retryWrites=true&w=majority'
mongo = MongoClient(app.config['MONGO_URI'])
db = mongo["test"]

recuperationTradeParFiltre = Blueprint('recuperationTradeParFiltre', __name__)

@recuperationTradeParFiltre.route('/recuperationTradeParFiltre', methods=['POST'])
def process_data():
    try:
        data = request.json
        collection = db[request.args.get('collection', None)]
        if isinstance(data, list):
            for item in data:
                if item and item.get('volume') is not None:
                    volume = item['volume']
                  
                if item and item.get('volume_remain') is not None:
                    volume_remain = item['volume_remain']
                  
                if item and item.get('profit') is not None:
                    profit = item['profit']
                  
                if item and item.get('symbol') is not None:
                    symbol = item['symbol']
                  
                if item and item.get('typeOfTransaction') is not None:
                    typeOfTransaction = item['typeOfTransaction']
                  
                if item and item.get('dateAndTimeOpening') is not None:
                    dateAndTimeOpening = item['dateAndTimeOpening']
                  
                if item and item.get('dateAndTimeClosure') is not None:
                    dateAndTimeClosure = item['dateAndTimeClosure']
                  
        query = {'$and': []}

        if volume is not None:
            query['$and'].append({'volume': volume})

        if volume_remain is not None:
            query['$and'].append({'volume_remain': volume_remain})

        if profit is not None:
            query['$and'].append({'profit': profit})

        if symbol is not None:
            query['$and'].append({'symbol': symbol})

        if typeOfTransaction is not None:
            query['$and'].append({'typeOfTransaction': typeOfTransaction})

        if dateAndTimeOpening is not None:
            query['$and'].append({'dateAndTimeOpening': dateAndTimeOpening})

        if dateAndTimeClosure is not None:
            query['$and'].append({'dateAndTimeClosure': dateAndTimeClosure})
          
        if len(query['$and']) > 0:
            data = list(collection.find(query))
        else:
            query = {}
            data = list(collection.find(query))
        data = json.loads(json.dumps(data, default=json_serial))
        return jsonify({'data': data})
    except Exception as e:
        current_app.logger.error(f"Error occurred: {e}")
        return jsonify({"error": "Erreur lors de la récupération des données par filtre, "details": str(e)}), 500
