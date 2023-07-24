from flask import Blueprint, jsonify, request
from flask_pymongo import PyMongo
import jwt
from bson import ObjectId

things_blueprint = Blueprint('things', __name__)

def convert_to_json_serializable(data):
    for key, value in data.items():
        if isinstance(value, bytes):
            data[key] = str(value)
        elif isinstance(value, ObjectId):
            data[key] = str(value)
        elif isinstance(value, dict):
            data[key] = convert_to_json_serializable(value)
    return data

def setup_things_routes(app):
    @things_blueprint.route('/recuperationTrade', methods=['GET'])
    def get_all_things():
        try:
            app.config['MONGO_URI'] = 'mongodb+srv://pierre:ztxiGZypi6BGDMSY@atlascluster.sbpp5xm.mongodb.net/test?retryWrites=true&w=majority'
            mongo = PyMongo(app)

            argUsername = request.args.get('username', None)
            argTypeTrade = request.args.get('typeTrade', None)

            query = {
                '$and': [
                    {'username': argUsername},
                ]
            }

            if argTypeTrade is not None and argTypeTrade == "renseigne":
                query['$and'].append({'$or': [{'annonceEconomique': {'$ne': None}}, {'psychologie': {'$ne': None}}, {'strategie': {'$ne': None}}]})
            if argTypeTrade is not None and argTypeTrade == "nonrenseigne":
                query['$and'].append({'$and': [{'annonceEconomique': None}, {'Fatigue': None}, {'psychologie': None}]})

            things_collection = mongo.db.things
            all_things = list(things_collection.find(query))

            for thing in all_things:
                thing = convert_to_json_serializable(thing)

            return jsonify(all_things), 200

        except Exception as e:
            return jsonify({"error": str(e)}), 500

    @things_blueprint.route('/updateTrade', methods=['POST'])
    def update_trade():
        try:
            app.config['MONGO_URI'] = 'mongodb+srv://pierre:ztxiGZypi6BGDMSY@atlascluster.sbpp5xm.mongodb.net/test?retryWrites=true&w=majority'
            mongo = PyMongo(app)

            data = request.get_json()
            trades_data = data.get('trades', [])

            things_collection = mongo.db.things  # Déplacez cette ligne en dehors de la boucle for

            for trade in trades_data:
                trade_id = trade.get('id')
                valeur_ann_eco = trade.get('valeurAnnEco')

                if trade_id and valeur_ann_eco in ['oui', 'non']:
                    annonce_economique = True if valeur_ann_eco == 'oui' else False

                    things_collection.update_one({'_id': ObjectId(trade_id)}, {'$set': {'annonceEconomique': annonce_economique}})

            return jsonify({"message": "Trade details updated successfully."}), 200

        except Exception as e:
            return jsonify({"error": str(e)}), 500

    return things_blueprint