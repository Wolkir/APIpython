from flask import Blueprint, jsonify, request, current_app
from flask_pymongo import PyMongo
from bson import ObjectId  # Importer ObjectId

recuperationStrategie = Blueprint('recuperationStrategie', __name__)

@recuperationStrategie.route('/recuperationStrategie', methods=['GET'])
def get_recuperationStrategie():
    try:
        username = request.args.get('username')

        if not username:
            return jsonify({"error": "L'argument 'username' est manquant dans la requête"}), 400

        mongo = PyMongo(current_app)
        collection = mongo.db['strategies']

        # Convertir les objets ObjectId en chaînes de caractères
        strategies = list(collection.find({"username": username}))
        for strategy in strategies:
            strategy['_id'] = str(strategy['_id'])

        return jsonify(strategies), 200

    except Exception as e:
        current_app.logger.error(f"Error occurred: {e}")
        return jsonify({"error": "Erreur lors de la récupération des stratégies pour l'utilisateur donné", "details": str(e)}), 500
