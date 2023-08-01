from flask import Blueprint, jsonify, request, current_app
from flask_pymongo import PyMongo
from bson import ObjectId

suppressionPorteFeuille = Blueprint('suppressionPorteFeuille', __name__)

@suppressionPorteFeuille.route('/suppressionPorteFeuille', methods=['DELETE'])
def delete_suppressionPorteFeuille():
    try:
        data = request.json
        nomPorteFeuille = data.get('nomPorteFeuille')

        if not nomPorteFeuille:
            return jsonify({"error": "Le nom de la collection 'nomPorteFeuille' est manquant dans la requête"}), 400

        mongo = PyMongo(current_app)
        db = mongo.db

        collections_to_delete = [name for name in db.list_collection_names() if name == nomPorteFeuille]

        for collection_name in collections_to_delete:
            db.drop_collection(collection_name)

        return jsonify({"message": f"Toutes les collections avec le nom '{nomPorteFeuille}' ont été supprimées avec succès."}), 200

    except Exception as e:
        current_app.logger.error(f"Error occurred: {e}")
        return jsonify({"error": "Erreur lors de la suppression des collections pour le nomPorteFeuille donné", "details": str(e)}), 500
