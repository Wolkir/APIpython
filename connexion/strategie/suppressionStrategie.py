from flask import Blueprint, jsonify, request, current_app
from flask_pymongo import PyMongo

suppressionStrategie = Blueprint('suppressionStrategie', __name__)

@suppressionStrategie.route('/suppressionStrategie', methods=['POST'])
def suppression_strategie():
    data = request.json

    if not data:
        return jsonify({"error": "Aucune donnée trouvée dans la requête"}), 400
        
    username = data.get('username')
    nomStrategie = data.get('nomStrategie')

    try:
        mongo = PyMongo(current_app)
        collection = mongo.db['strategies']

        result = collection.delete_many({"nomStrategie": nomStrategie})

        if result.deleted_count > 0:
            return jsonify({"message": "Stratégie supprimée avec succès"}), 200
        else:
            return jsonify({"error": "La stratégie n'a pas été trouvée"}), 404

    except Exception as e:
        current_app.logger.error(f"Error occurred: {e}")
        return jsonify({"error": "Erreur lors de la enregistrement des stratégies pour l'utilisateur donné", "details": str(e)}), 500
