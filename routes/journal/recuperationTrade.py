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

            things_collection = mongo.db.things
            all_things = list(things_collection.find({}))

            for thing in all_things:
                thing = convert_to_json_serializable(thing)

            return jsonify(all_things), 200

        except Exception as e:
            return jsonify({"error": str(e)}), 500

    return things_blueprint
