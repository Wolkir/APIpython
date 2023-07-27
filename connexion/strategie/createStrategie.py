from flask import Blueprint, jsonify, request, current_app
from flask_pymongo import PyMongo

createStrategie = Blueprint('createStrategie', __name__)

def setup_createStrategie_routes(app):
    app.config['MONGO_URI'] = 'mongodb://pierre:ztxiGZypi6BGDMSY@atlascluster.sbpp5xm.mongodb.net/test?retryWrites=true&w=majority'
    mongo = PyMongo(app)

    @createStrategie.route('/createStrategie', methods=['POST'])
    def create_strategie():
        data = request.json
        username = data.get('username')
        nomStrategie = data.get('nomStrategie')

        try:
            existing_strategie = mongo.db.strategies.find_one({"nomStrategie": nomStrategie})
            if existing_strategie:
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
