from flask import Blueprint, jsonify, request
from flask_pymongo import PyMongo

# Créez le blueprint
recuperationStrategie = Blueprint('recuperationStrategie', __name__)

# Définissez la fonction pour récupérer les stratégies
@recuperationStrategie.route('/recuperationStrategie', methods=['GET'])
def recuperationStrategieGet():
    try:
        # Récupérer l'argument "username" de la requête
        username = request.args.get('username')

        if not username:
            return jsonify({"error": "L'argument 'username' est manquant dans la requête"}), 400

        # Connexion à la base de données MongoDB
        app = recuperationStrategie.app
        app.config['MONGO_URI'] = 'mongodb://pierre:ztxiGZypi6BGDMSY@atlascluster.sbpp5xm.mongodb.net/test?retryWrites=true&w=majority'
        mongo = PyMongo(app)
        collection = mongo.db['strategies']

        # Récupérer les données de la base de données pour l'utilisateur donné
        strategies = list(collection.find({"username": username}))

        return jsonify(strategies), 200

    except Exception as e:
        current_app.logger.error(f"Error occurred: {e}")
        return jsonify({"error": "Erreur lors de la récupération des stratégies pour l'utilisateur donné", "details": str(e)}), 500
