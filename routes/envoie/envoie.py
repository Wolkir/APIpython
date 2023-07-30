from flask import Blueprint, jsonify, request, current_app
from flask import Flask
import logging
import atexit
import json
from datetime import datetime, timedelta

from bson import ObjectId
from dns.rdatatype import NULL
from pymongo import MongoClient
from pymongo.errors import PyMongoError

from .date import process_argument_date
from .XY import process_argument_xyTPR
from .XY import process_argument_xySL
from .XY import process_argument_xyBE
from .XY import process_argument_xySortieManuelle
from .XY import process_argument_xyTilt

client = MongoClient('mongodb+srv://pierre:ztxiGZypi6BGDMSY@atlascluster.sbpp5xm.mongodb.net/?retryWrites=true&w=majority')
envoie = Blueprint('envoie', __name__)
app = Flask(__name__)

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

def process_argument_value(arg):
    if arg == "" or arg == None:
        return None
    return arg

@envoie.route('/envoie', methods=['GET'])
def update_envoie():
    argD = process_argument_value(request.args.get('argD', None))
    argI = process_argument_value(request.args.get('argI', None))
    debutDate = request.args.get('argSD', None)
    finDate = request.args.get('argED', None)
    username = request.args.get('username', None)
    argTPR = process_argument_value(request.args.get('argTPR', None))
    argSL = process_argument_value(request.args.get('argSL', None))
    argBE = process_argument_value(request.args.get('argBE', None))
    argPsy = process_argument_value(request.args.get('argPsy', None))
    argStrat = process_argument_value(request.args.get('argStrat', None))
    argAnnEco = process_argument_value(request.args.get('argAnnEco', None))
    argPos = process_argument_value(request.args.get('argPos', None))
    argTypOrd = process_argument_value(request.args.get('argTypOrd', None))
    argSortManu = process_argument_value(request.args.get('argSortManu', None))
    argTilt = process_argument_value(request.args.get('argTilt', None))
    
    db = client['test']
    collection = db['things']

    start_date, end_date = process_argument_date(argD, debutDate, finDate)
    
    argTPRbinaire = None
    argSLbinaire = None
    argBEbinaire = None
    argSortManuBinaire = None
    argTiltBinaire = None

    if argTPR is not None:
        argTPRbinaire = process_argument_xyTPR(argTPR)
    if argSL is not None:
        argSLbinaire = process_argument_xySL(argSL)
    if argBE is not None:
        argBEbinaire = process_argument_xyBE(argBE)
    if argSortManu is not None:
        argSortManuBinaire = process_argument_xySortieManuelle(argSortManu)
    if argTilt is not None:
        argTiltBinaire = process_argument_xyTilt(argTilt)

    try:
        query = {'$and': []}

        # username
        if username is not None:
            query['$and'].append({'username': username})

        # tilt
        if argTiltBinaire is not None:
            query['$and'].append({'journeeDeTilt': argTiltBinaire})

        # sortie manuelle
        if argSortManuBinaire is not None:
            query['$and'].append({'sortieManuelle': argSortManuBinaire})

        # date
        if start_date is not None and end_date is not None:
            query['$and'].append({'dateAndTimeOpening': {'$gte': start_date, '$lt': end_date}})

        # indice
        if argI is not None:
            query['$and'].append({'symbole': argI})

        # TPR
        if argTPRbinaire is not None:
            query['$and'].append({'TPR': argTPRbinaire})

        # SL
        if argSLbinaire is not None:
            query['$and'].append({'slr': argSLbinaire})

        # BE
        if argBEbinaire is not None:
            query['$and'].append({'slr': argBEbinaire})

        # psy
        if argPsy is not None:
            query['$and'].append({'psychologie': argPsy})

        # strat
        if argStrat is not None:
            query['$and'].append({'strategie': argStrat})

        # annonce economique
        if argAnnEco is not None:
            query['$and'].append({'annonceEconomique': argAnnEco})

        # position
        if argPos is not None:
            query['$and'].append({'position': argPos})

        # type ordre
        if argTypOrd is not None:
            query['$and'].append({'typeOrdre': argTypOrd})

        data = list(collection.find(query))
        data = json.loads(json.dumps(data, default=json_serial))

        return jsonify({'data': data})
    except Exception as e:
        current_app.logger.error(f"Error occurred: {e}")
        return jsonify({"error": "Erreur lors de la enregistrement des stratégies pour l'utilisateur donné", "details": str(e)}), 500
