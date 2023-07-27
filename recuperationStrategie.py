from flask import Blueprint, jsonify, request
from flask_pymongo import PyMongo

recuperationStrategie = Blueprint('recuperationStrategie', __name__)

@recuperationStrategie.route('/recuperationStrategie', methods=['GET'])
def get_recuperationStrategie():
    try:
        username = request.args.get('username')

        if not username:
            return jsonify({"error": "L'argument 'username' est manquant dans la requête"}), 400

        mongo = PyMongo(app)  # En supposant que "app" est défini dans server.py
        collection = mongo.db['strategies']

        strategies = list(collection.find({"username": username}))

        return jsonify(strategies), 200

    except Exception as e:
        return jsonify({"error": "Erreur lors de la récupération des stratégies pour l'utilisateur donné", "details": str(e)}), 500

def setup_recuperationStrategie(app):
    # Vous pouvez effectuer d'autres opérations si nécessaire
    # avant de retourner le blueprint
    return recuperationStrategie
