from flask import Blueprint, jsonify, request, current_app
from flask_pymongo import PyMongo

createPorteFeuille = Blueprint('createPorteFeuille', __name__)

@createPorteFeuille.route('/createPorteFeuille', methods=['POST'])
def create_PorteFeuille():
    data = request.json
    username = data.get('username')
    nomPorteFeuille = data.get('nomPorteFeuille')

    nomCompletPorteFeuille = username + "_" + nomPorteFeuille

    try:
        mongo = PyMongo(current_app)
        db = mongo.db
        
        if nomCompletPorteFeuille in db.list_collection_names():
            return jsonify({"error": "Cette indicateur existe déjà"}), 400
        else:
            db.create_collection(nomCompletPorteFeuille)
            return jsonify({"message": "portefeuille enregistrée avec succès"}), 200
    except Exception as e:
        current_app.logger.error(f"Error occurred: {e}")
        return jsonify({"error": "Erreur lors de la enregistrement des indicateurs pour l'utilisateur donné", "details": str(e)}), 500
