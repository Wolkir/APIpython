from flask import Blueprint, jsonify, request
from flask_pymongo import PyMongo
import jwt

things_blueprint = Blueprint('things', __name__)

def setup_things_routes(app):
    @things_blueprint.route('/recuperationTrade', methods=['GET'])
    def get_all_things():
        try:
            app.config['MONGO_URI'] = 'mongodb+srv://pierre:ztxiGZypi6BGDMSY@atlascluster.sbpp5xm.mongodb.net/test?retryWrites=true&w=majority'
            mongo = PyMongo(app)

            things_collection = mongo.db.things
            all_things = list(things_collection.find({}))

            for thing in all_things:
                thing['_id'] = str(thing['_id'])

            return jsonify(all_things), 200

        except Exception as e:
            return jsonify({"error": str(e)}), 500

    return things_blueprint
