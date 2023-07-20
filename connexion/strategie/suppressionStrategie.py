from flask import Blueprint, jsonify, request
from flask_pymongo import PyMongo

suppressionStrategie = Blueprint('suppressionStrategie', __name__)

@suppressionStrategie.route('/suppressionStrategie', methods=['POST'])
def suppression_strategie(app):
    data = request.json
    username = data.get('username')
    nomStrategie = data.get('nomStrategie')

    try:
        app.config['MONGO_URI'] = 'mongodb://pierre:ztxiGZypi6BGDMSY@atlascluster.sbpp5xm.mongodb.net/test?retryWrites=true&w=majority'
        mongo = PyMongo(app)
        collection = mongo.db['strategies']

        result = collection.delete_many({"nomStrategie": nomStrategie})

        if result.deleted_count > 0:
            return jsonify({"message": "Stratégie supprimée avec succès"}), 200
        else:
            return jsonify({"error": "La stratégie n'a pas été trouvée"}), 404

    except Exception as e:
        return jsonify({"error": "Erreur lors de la suppression de la stratégie"}), 500
