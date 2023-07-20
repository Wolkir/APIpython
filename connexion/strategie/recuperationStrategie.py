from flask import Blueprint, jsonify
from flask_pymongo import PyMongo

recuperationStrategie = Blueprint('recuperationStrategie', __name__)

def setup_recuperationStrategie_routes(app):
    app.config['MONGO_URI'] = 'mongodb://pierre:ztxiGZypi6BGDMSY@atlascluster.sbpp5xm.mongodb.net/test?retryWrites=true&w=majority'
    mongo = PyMongo(app)

    @recuperationStrategie.route('/recuperationstrategie/<username>', methods=['GET'])
    def recuperation_strategie(username):
        try:
            # Connexion à la base de données MongoDB
            app.config['MONGO_URI'] = 'mongodb://pierre:ztxiGZypi6BGDMSY@atlascluster.sbpp5xm.mongodb.net/test?retryWrites=true&w=majority'
            mongo = PyMongo(app)
            collection = mongo.db['strategies']

            # Récupération des stratégies pour l'utilisateur donné
            strategies = list(collection.find({"username": username}))

            return jsonify(strategies), 200

        except Exception as e:
            return jsonify({"error": "Erreur lors de la récupération des stratégies"}), 500
