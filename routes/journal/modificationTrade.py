from flask import Blueprint, jsonify, request
from flask_pymongo import PyMongo
import jwt
from bson import ObjectId


modificationTrade = Blueprint('modificationTrade', __name__)

def convert_to_json_serializable(data):
    for key, value in data.items():
        if isinstance(value, bytes):
            data[key] = str(value)
        elif isinstance(value, ObjectId):
            data[key] = str(value)
        elif isinstance(value, dict):
            data[key] = convert_to_json_serializable(value)
    return data

def setup_modificationTrade_routes(app):

    @modificationTrade.route('/modificationTrade', methods=['POST'])
    def update_trade():
        try:
            app.config['MONGO_URI'] = 'mongodb+srv://pierre:ztxiGZypi6BGDMSY@atlascluster.sbpp5xm.mongodb.net/test?retryWrites=true&w=majority'
            mongo = PyMongo(app)
            data = request.get_json()
            trades_data = data.get('trades', [])
            psychologie_data = data.get('psychologie', [])
            position_data = data.get('position', [])
            things_collection = mongo.db.things

            # Mise à jour ou création des champs psychologie
            for psychologie_item in psychologie_data:
                trade_id = psychologie_item.get('id')
                value_psy = psychologie_item.get('valuePsy')

                if trade_id and value_psy:
                    things_collection.update_one({'_id': ObjectId(trade_id)}, {'$set': {'psychologie': value_psy}}, upsert=True)
            
            # Mise à jour du champ annonceEconomique
            for trade in trades_data:
                trade_id = trade.get('id')
                valeur_ann_eco = trade.get('valeurAnnEco')

                if trade_id and valeur_ann_eco in ['oui', 'non']:
                    annonce_economique = True if valeur_ann_eco == 'oui' else False

                    things_collection.update_one({'_id': ObjectId(trade_id)}, {'$set': {'annonceEconomique': annonce_economique}})
            # Mise à jour du champ position
            for position in position_data:
                trade_id = position.get('id')
                valeur_position = position.get('valuePosition')

                if trade_id and valeur_position:
                    things_collection.update_one({'_id': ObjectId(trade_id)}, {'$set': {'position': valeur_position}})

            return jsonify({"message": "Trade details updated successfully."}), 200

        except Exception as e:
            return jsonify({"error": str(e)}), 500

    return modificationTrade


