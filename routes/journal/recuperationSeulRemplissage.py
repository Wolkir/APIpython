from flask import Blueprint, jsonify, request, current_app
from flask_pymongo import PyMongo
from bson import ObjectId

recuperationSeulRemplissage = Blueprint('recuperationSeulRemplissage', __name__)

@recuperationSeulRemplissage.route('/recuperationSeulRemplissage', methods=['GET'])
def get_recuperationSeulRemplissage():
    try:
        username = request.args.get('username')
        nomRemplissageDefaut = request.args.get('nomRemplissageDefaut')

        if not username:
            return jsonify({"error": "L'argument 'username' est manquant dans la requête"}), 400

        mongo = PyMongo(current_app)
        collection_brut = 'remplissageDefaut'
        collection = mongo.db[collection_brut]

        remplissageDefaut = list(collection.find({"username": username, "nomRemplissageDefaut": nomRemplissageDefaut}))
        for strategy in remplissageDefaut:
            strategy['_id'] = str(strategy['_id'])

        return jsonify(remplissageDefaut), 200

    except Exception as e:
        current_app.logger.error(f"Error occurred: {e}")
        return jsonify({"error": "Erreur lors de la récupération du remplissage seul", "details": str(e)}), 500

