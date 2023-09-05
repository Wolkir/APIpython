from flask import Blueprint, jsonify, request, current_app
from flask_pymongo import PyMongo

createStrategie = Blueprint('createStrategie', __name__)

@createStrategie.route('/createStrategie', methods=['POST'])
def create_strategie():
    data = request.json
    username = data.get('username')
    nomStrategie = data.get('nomStrategie')

    try:
        mongo = PyMongo(current_app)
        collection = mongo.db['strategies']
        strategies = list(collection.find({"nomStrategie": nomStrategie, "username": username}))

        if strategies:
            return jsonify({"error": "Cette stratégie existe déjà"}), 400

        strategie = {
            "nomStrategie": nomStrategie,
            "username": username
        }
        mongo.db.strategies.insert_one(strategie)

        return jsonify({"message": "Stratégie enregistrée avec succès"}), 200
    except Exception as e:
        current_app.logger.error(f"Error occurred: {e}")
        return jsonify({"error": "Erreur lors de la enregistrement des stratégies pour l'utilisateur donné", "details": str(e)}), 500
