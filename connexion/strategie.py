# strategie_routes.py
from flask import Blueprint, jsonify, request
from flask_pymongo import PyMongo

strategie_blueprint = Blueprint('strategie', __name__)

def setup_strategie_routes(app):
    app.config['MONGO_URI'] = 'mongodb://pierre:ztxiGZypi6BGDMSY@atlascluster.sbpp5xm.mongodb.net/test?retryWrites=true&w=majority'
    mongo = PyMongo(app)

    @strategie_blueprint.route('/createstrategie', methods=['POST'])
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
            return jsonify({"error": "Erreur lors de l'enregistrement de la stratégie", "details": str(e)}), 500

    @strategie_blueprint.route('/suppressionstrategie', methods=['POST'])
    def suppression_strategie():
        data = request.json
        username = data.get('username')
        nomStrategie = data.get('nomStrategie')

        try:
            mongo.db.strategies.delete_many({"nomStrategie": nomStrategie})
            return jsonify({"message": "Stratégie supprimée avec succès"}), 200
        except Exception as e:
            return jsonify({"error": "Erreur lors de la suppression de la stratégie"}), 500

    @strategie_blueprint.route('/recuperationstrategie/<username>', methods=['GET'])
    def recuperation_strategie(username):
        try:
            strategies = list(mongo.db.strategies.find({"username": username}))
            return jsonify(strategies), 200
        except Exception as e:
            return jsonify({"error": "Erreur lors de la récupération des stratégies"}), 500
