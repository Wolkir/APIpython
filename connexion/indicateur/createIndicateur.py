from flask import Blueprint, jsonify, request, current_app
from flask_pymongo import PyMongo

createIndicateur = Blueprint('createIndicateur', __name__)

@createIndicateur.route('/createIndicateur', methods=['POST'])
def create_indicateur():
    data = request.json
    username = data.get('username')
    nomIndicateur = data.get('nomIndicateur')

    try:
        mongo = PyMongo(current_app)
        collection = mongo.db['indicateurs']
        indicateurs = list(collection.find({"nomIndicateur": nomIndicateur}, {"username": username}))
        if indicateurs:
            return jsonify({"error": "Cette indicateur existe déjà"}), 400

        indicateurs = {
            "nomIndicateur": nomIndicateur,
            "username": username
        }
        mongo.db.indicateurs.insert_one(indicateurs)

        return jsonify({"message": "indicateur enregistrée avec succès"}), 200
    except Exception as e:
        current_app.logger.error(f"Error occurred: {e}")
        return jsonify({"error": "Erreur lors de la enregistrement des indicateur pour l'utilisateur donné", "details": str(e)}), 500
