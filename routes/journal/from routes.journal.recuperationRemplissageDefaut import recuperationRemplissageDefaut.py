from flask import Blueprint, jsonify, request, current_app
from flask_pymongo import PyMongo
from bson import ObjectId

recuperationRemplissageDefaut = Blueprint('recuperationRemplissageDefaut', __name__)

@recuperationRemplissageDefaut.route('/recuperationRemplissageDefaut', methods=['GET'])
def get_recuperationRemplissageDefaut():
    try:
        username = request.args.get('username')

        if not username:
            return jsonify({"error": "L'argument 'username' est manquant dans la requête"}), 400

        mongo = PyMongo(current_app)
        collection = 'remplissageDefaut'
        collection = mongo.db[collection]

        remplissageDefaut = list(collection.find({"username": username}))
        for strategy in remplissageDefaut:
            strategy['_id'] = str(strategy['_id'])

        return jsonify(remplissageDefaut), 200

    except Exception as e:
        current_app.logger.error(f"Error occurred: {e}")
        return jsonify({"error": "Erreur lors de la récupération des stratégies pour l'utilisateur donné", "details": str(e)}), 500
