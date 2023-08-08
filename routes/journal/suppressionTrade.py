from flask import Blueprint, jsonify, request, current_app
from flask_pymongo import PyMongo
from bson import ObjectId

suppressionTrade = Blueprint('suppressionTrade', __name__)

@suppressionTrade.route('/suppressionTrade', methods=['DELETE'])
def delete_suppressionTrade():
    try:
        data = request.json
        collection = data.get('collection')
        id_str = data.get('id')

        if not collection or not id_str:
            return jsonify({"error": "Le nom de la collection ou l'id sont manquants dans la requête"}), 400

        try:
            id = ObjectId(id_str)
        except:
            return jsonify({"error": "L'ID fourni n'est pas valide"}), 400

        mongo = PyMongo(current_app)
        collectionDefinitive = mongo.db[collection]

        result = collectionDefinitive.delete_one({"_id": id})

        if result.deleted_count > 0:
            return jsonify({"message": "Trade supprimé avec succès"}), 200
        else:
            return jsonify({"error": "Le trade n'a pas été trouvé"}), 404

    except Exception as e:
        current_app.logger.error(f"Error occurred: {e}")
        return jsonify({"error": "Erreur lors de la suppression du trade", "details": str(e)}), 500
