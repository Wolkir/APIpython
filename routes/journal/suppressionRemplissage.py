from flask import Blueprint, jsonify, request, current_app
from flask_pymongo import PyMongo

suppressionRemplissage = Blueprint('suppressionRemplissage', __name__)

@suppressionRemplissage.route('/suppressionRemplissage', methods=['DELETE'])
def suppression_remplissage():
    data = request.json

    if not data:
        return jsonify({"error": "Aucune donnée trouvée dans la requête"}), 400
        
    username = data.get('username')
    nomRemplissageDefaut = data.get('nomRemplissageDefaut')

    try:
        mongo = PyMongo(current_app)

        collection = mongo.db['remplissageDefaut']

        result = collection.delete_many({"nomRemplissageDefaut": nomRemplissageDefaut, "username": username})

        if result.deleted_count > 0:
            return jsonify({"message": "Repmlissage supprimée avec succès"}), 200
        else:
            return jsonify({"error": "Le Repmlissage n'a pas été trouvée"}), 404

    except Exception as e:
        current_app.logger.error(f"Error occurred: {e}")
        return jsonify({"error": "Erreur lors de la suppression du Repmlissage", "details": str(e)}), 500
