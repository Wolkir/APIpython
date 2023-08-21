from flask import Blueprint, jsonify, request, current_app
from flask_pymongo import PyMongo
from bson import ObjectId

recuperationPorteFeuille = Blueprint('recuperationPorteFeuille', __name__)

@recuperationPorteFeuille.route('/recuperationPorteFeuille', methods=['GET'])
def get_recuperationPorteFeuille():
    try:
        username = request.args.get('username')

        mongo = PyMongo(current_app)
        db = mongo.db

        if not username:
            return jsonify({"error": "L'argument 'username' est manquant dans la requête"}), 400
        
        exception = "utile"

        collections = [name for name in db.list_collection_names() if username in name and exception not in name.split('_')]

        data = [{"nomSeul": collection.replace("_" + username, "").replace(username + "_", "").replace(username, ""), "nomComplet": collection} for collection in collections]

        return jsonify(data), 200

    except Exception as e:
        current_app.logger.error(f"Error occurred: {e}")
        return jsonify({"error": "Erreur lors de la récupération des indicateurs pour l'utilisateur donné", "details": str(e)}), 500
