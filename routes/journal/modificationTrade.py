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
            typeOrdre_data = data.get('typeOrdre', [])
            violeStrategie_data = data.get('violeStrategie', [])
            sortie_data = data.get('sortie', [])
            indicateur1_data = data.get('indicateur1', [])
            indicateur2_data = data.get('indicateur2', [])
            indicateur3_data = data.get('indicateur3', [])
            strategie_data = data.get('strategie', [])
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
            
            # Mise à jour du champ type ordre
            for typeOrdre in typeOrdre_data:
                trade_id = typeOrdre.get('id')
                valeur_typeOrdre = typeOrdre.get('valueTypeOrdre')

                if trade_id and valeur_typeOrdre:
                    things_collection.update_one({'_id': ObjectId(trade_id)}, {'$set': {'typeOrdre': valeur_typeOrdre}})

            # Mise à jour du champ violeStrategie
            for viole in violeStrategie_data:
                trade_id = viole.get('id')
                valeur_violeStrategie = viole.get('valueVioleStrategie')

                if trade_id and valeur_violeStrategie in ['oui', 'non']:
                    violeStrategie = True if valeur_violeStrategie == 'oui' else False
                    things_collection.update_one({'_id': ObjectId(trade_id)}, {'$set': {'violeStrategie': violeStrategie}})
            
            # Mise à jour du champ sortie
            for sortie in sortie_data:
                trade_id = sortie.get('id')
                valeur_sortie = sortie.get('valueSortie')

                if trade_id and valeur_sortie:
                    things_collection.update_one({'_id': ObjectId(trade_id)}, {'$set': {'sortie': valeur_sortie}})

            # Mise à jour ou création des champs indicateur1
            for indicateur1_item in indicateur1_data:
                trade_id = indicateur1_item.get('id')
                value_indicateur1 = indicateur1_item.get('valueIndicateur1')

                if trade_id and value_indicateur1:
                    things_collection.update_one({'_id': ObjectId(trade_id)}, {'$set': {'indicateur1': value_indicateur1}}, upsert=True)

            # Mise à jour ou création des champs indicateur2
            for indicateur2_item in indicateur2_data:
                trade_id = indicateur2_item.get('id')
                value_indicateur2 = indicateur2_item.get('valueIndicateur2')

                if trade_id and value_indicateur2:
                    things_collection.update_one({'_id': ObjectId(trade_id)}, {'$set': {'indicateur2': value_indicateur2}}, upsert=True)

            # Mise à jour ou création des champs indicateur3
            for indicateur3_item in indicateur3_data:
                trade_id = indicateur3_item.get('id')
                value_indicateur3 = indicateur3_item.get('valueIndicateur3')

                if trade_id and value_indicateur3:
                    things_collection.update_one({'_id': ObjectId(trade_id)}, {'$set': {'indicateur3': value_indicateur3}}, upsert=True)

            # Mise à jour ou création des champs strategie
            for strategie_item in strategie_data:
                trade_id = strategie_item.get('id')
                value_strategie = strategie_item.get('valueStrategie')

                if trade_id and value_strategie:
                    things_collection.update_one({'_id': ObjectId(trade_id)}, {'$set': {'strategie': value_strategie}}, upsert=True)

            return jsonify({"message": "Trade details updated successfully."}), 200

        except Exception as e:
            return jsonify({"error": str(e)}), 500

    return modificationTrade
