from flask import Blueprint, jsonify, request, current_app
from flask_pymongo import PyMongo
import jwt
from bson.objectid import ObjectId

recuperationUnTrade = Blueprint('recuperationUnTrade', __name__)

def convert_to_json_serializable(data):
    for key, value in data.items():
        if isinstance(value, bytes):
            data[key] = str(value)
        elif isinstance(value, ObjectId):
            data[key] = str(value)
        elif isinstance(value, dict):
            data[key] = convert_to_json_serializable(value)
    return data

def recuperation_un_seul_trade(app):
    @recuperationUnTrade.route('/recuperationUnTrade', methods=['GET'])
    def recuperation_un_trade():
        try:
            mongo = PyMongo(current_app)

            arg_id = request.args.get('id')
            obj_id = ObjectId(arg_id)
            argCollection = request.args.get('collection', None)

            query = {
                '$and': [
                    {'_id': obj_id},
                ]
            }

            things_collection = mongo.db[argCollection]
            resultat = list(things_collection.find(query))

            result = []
            for thing in resultat:
                converted_thing = convert_to_json_serializable(thing)
                result.append(converted_thing)

            return jsonify(result), 200

        except Exception as e:
            current_app.logger.error(f"Error occurred: {e}")
            return jsonify({"error": str(e)}), 500
        
    return recuperationUnTrade
