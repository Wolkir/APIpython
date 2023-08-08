from flask import Blueprint, jsonify, request, current_app
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
            mongo = PyMongo(current_app)
            db = mongo.db

            argUsername = request.args.get('username', None)
            argTypeTrade = request.args.get('typeTrade', None)
            argCollection = request.args.get('collection', None)

            collection = argCollection

            collection = argCollection
            query = {
                '$and': [
                    {'username': argUsername},
                ]
            }

            if argTypeTrade is not None and argTypeTrade == "renseigne":
                query['$and'].append({'$or': [{'annonceEconomique': {'$ne': None}}, {'psychologie': {'$ne': None}}, {'strategie': {'$ne': None}}]})
            if argTypeTrade is not None and argTypeTrade == "nonrenseigne":
                query['$and'].append({'$and': [{'annonceEconomique': None}, {'Fatigue': None}, {'psychologie': None}]})

            things_collection = mongo.db[collection]
            all_things = list(things_collection.find(query))

            result = []
            for thing in all_things:
                thing = convert_to_json_serializable(thing)
                thing['collection'] = collection
                result.append(thing)

            return jsonify(result), 200

        except Exception as e:
            return jsonify({"error": str(e)}), 500

    @things_blueprint.route('/suppressionTrade', methods=['DELETE'])
    def delete_suppressionTrade():
        try:
            data = request.json
            collection = data.get('collection')
            id_str = data.get('id')
    
            if not collection or not id_str:
                return jsonify({"error": "Le nom de la collection ou l'id sont manquants dans la requête"}), 400
    
            try:
                id = ObjectId(id_str)
            except:
                return jsonify({"error": "L'ID fourni n'est pas valide"}), 400
    
            mongo = PyMongo(current_app)
            collectionDefinitive = mongo.db[collection]
    
            result = collectionDefinitive.delete_one({"_id": id})
    
            if result.deleted_count > 0:
                return jsonify({"message": "Trade supprimé avec succès"}), 200
            else:
                return jsonify({"error": "Le trade n'a pas été trouvé"}), 500
    
        except Exception as e:
            current_app.logger.error(f"Error occurred: {e}")
            return jsonify({"error": "Erreur lors de la suppression du trade", "details": str(e)}), 500
        
    return things_blueprint

