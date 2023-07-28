from flask import Blueprint, jsonify, request, current_app
from flask_pymongo import PyMongo
from bson import ObjectId  # Importer ObjectId

recuperationIndicateur = Blueprint('recuperationIndicateur', __name__)

@recuperationIndicateur.route('/recuperationIndicateur', methods=['GET'])
def get_recuperationIndicateur():
    try:
        username = request.args.get('username')

        if not username:
            return jsonify({"error": "L'argument 'username' est manquant dans la requête"}), 400

        mongo = PyMongo(current_app)
        collection = mongo.db['indicateurs']

        indicateurs = list(collection.find({"username": username}))
        for indicateur in indicateurs:
            indicateur['_id'] = str(indicateur['_id'])

        return jsonify(indicateurs), 200

    except Exception as e:
        current_app.logger.error(f"Error occurred: {e}")
        return jsonify({"error": "Erreur lors de la récupération des indicateurs pour l'utilisateur donné", "details": str(e)}), 500