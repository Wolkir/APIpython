from flask import Blueprint, jsonify, request, current_app
from flask_pymongo import PyMongo

suppressionIndicateur = Blueprint('suppressionIndicateur', __name__)

@suppressionIndicateur.route('/suppressionIndicateur', methods=['DELETE'])
def suppression_indicateur():
    data = request.json

    if not data:
        return jsonify({"error": "Aucune donnée trouvée dans la requête"}), 400
        
    username = data.get('username')
    nomIndicateur = data.get('nomIndicateur')

    try:
        mongo = PyMongo(current_app)
        collection = mongo.db['indicateurs']

        result = collection.delete_many({"nomIndicateur": nomIndicateur})

        if result.deleted_count > 0:
            return jsonify({"message": "indicateurs supprimée avec succès"}), 200
        else:
            return jsonify({"error": "La indicateurs n'a pas été trouvée"}), 404

    except Exception as e:
        current_app.logger.error(f"Error occurred: {e}")
        return jsonify({"error": "Erreur lors de la enregistrement des indicateurs pour l'utilisateur donné", "details": str(e)}), 500