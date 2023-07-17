from flask import Blueprint, jsonify, request

import atexit
import json
from datetime import datetime, timedelta

from bson import ObjectId
from dns.rdatatype import NULL
from pymongo import MongoClient
from pymongo.errors import PyMongoError

from .date import process_argument_date
#from .indice import process_argument_indice
from .XY import process_argument_xy

client = MongoClient('mongodb+srv://pierre:ztxiGZypi6BGDMSY@atlascluster.sbpp5xm.mongodb.net/?retryWrites=true&w=majority')
envoie = Blueprint('envoie', __name__)

def json_serial(obj):
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

@envoie.route('/envoie', methods=['GET'])
def update_envoie():
    argD = request.args.get('argD', None)
    argI = request.args.get('argI', None)
    debutDate = request.args.get('argSD', None)
    finDate = request.args.get('argED', None)
    argTPR = request.args.get('argTPR', None)
    argSL = request.args.get('argSL', None)
    argBE = request.args.get('argBE', None)
    argPsy = request.args.get('argPsy', None)
    argStrat = request.args.get('argStrat', None)
    argAnnEco = request.args.get('argAnnEco', None)
    argPos = request.args.get('argPos', None)
    argTypOrd = request.args.get('argTypOrd', None)

    print("argD : " + argD)
    print("argI : " + argI)
    print("argTPR : " + argTPR)
    print("argSL : " + argSL)
    print("argBE : " + argBE)
    print("argPsy : " + argPsy)
    print("argStrat : " + argStrat)
    print("argAnnEco : " + argAnnEco)
    print("argPos : " + argPos)
    print("argTypOrd : " + argTypOrd)
    
    db = client['test']
    collection = db['thingsTest']

    start_date, end_date = process_argument_date(argD, debutDate, finDate)
    if start_date is None or end_date is None:
        return jsonify({'message': 'Invalid date arguments date'})
    print(start_date, end_date)
    
    argTPRbinaire, argSLbinaire, argBEbinaire = process_argument_xy(argTPR, argSL, argBE)
    if argTPRbinaire is None and argSLbinaire is None and argBEbinaire is None:
        print("ereaca")
        return jsonify({'message': 'Invalid argument tpr sl be'})

    try:
        query = {
            '$and': [
                {'dateAndTimeOpening': {'$gte': start_date, '$lt': end_date}},
                {'symbole': argI}
            ]
        }

        if argI is not None:
            query['$and'].append({'symbole': argI})
        if argTPRbinaire is not None:
            query['$and'].append({'TPR': argTPRbinaire})
        if argSLbinaire is not None:
            query['$and'].append({'slr': argSLbinaire})
        if argBEbinaire is not None:
            query['$and'].append({'slr': argBEbinaire})
        if argPsy is not None:
            query['$and'].append({'psychologie': argPsy})
        if argStrat is not None:
            query['$and'].append({'strategie': argStrat})
        if argAnnEco is not None:
            query['$and'].append({'annonceEconomique': argAnnEco})
        if argPos is not None:
            query['$and'].append({'position': argPos})
        if argTypOrd is not None:
            query['$and'].append({'typeOrdre': argTypOrd})

        data = list(collection.find(query))
        data = json.loads(json.dumps(data, default=json_serial))

        return jsonify({'data': data})
    except PyMongoError as e:
        print("An error occurred:", str(e))
        return jsonify({'message': 'Error occurred'})
