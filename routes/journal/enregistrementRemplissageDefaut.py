from flask import Blueprint, jsonify, request, current_app
from flask_pymongo import PyMongo

enregistrementRemplissageDefaut = Blueprint('enregistrementRemplissageDefaut', __name__)

@enregistrementRemplissageDefaut.route('/enregistrementRemplissageDefaut', methods=['POST'])
def create_enregistrementRemplissageDefaut():
    data = request.get_json()
    psychologie_data = data.get('psychologie', [])
    position_data = data.get('position', [])
    typeOrdre_data = data.get('typeOrdre', [])
    violeStrategie_data = data.get('violeStrategie', [])
    sortie_data = data.get('sortie', [])
    indicateur1_data = data.get('indicateur1', [])
    indicateur2_data = data.get('indicateur2', [])
    indicateur3_data = data.get('indicateur3', [])
    strategie_data = data.get('strategie', [])
    timeEntree_data = data.get('timeEntree', [])
    timeSetup_data = data.get('timeSetup', [])
    nomRemplissageDefaut_data = data.get('nomRemplissageDefaut', [])
    username = data.get('username', [])

    collection = "remplissageDefaut"

    try:
        mongo = PyMongo(current_app)
        collection = mongo.db[collection]
        verificationExiste = list(collection.find({"nomRemplissageDefaut": nomRemplissageDefaut_data}, {"username": username}))

        if not verificationExiste:
            nouveauDocument = {
                "psychologie": psychologie_data,
                "position": position_data,
                "typeOrdre": typeOrdre_data,
                "violeStrategie": violeStrategie_data,
                "sortie": sortie_data,
                "indicateur1": indicateur1_data,
                "indicateur2": indicateur2_data,
                "indicateur3": indicateur3_data,
                "strategie": strategie_data,
                "timeEntree": timeEntree_data,
                "timeSetup": timeSetup_data,
                "nomRemplissageDefaut": nomRemplissageDefaut_data,
                "username": username
            }
            collection.insert_one(nouveauDocument)
            return jsonify({"message": "Remplissage par défaut enregistrée avec succès"}), 200
        else:
            return jsonify({"message": "Ce remplissage par défaut existe déjà"}), 200

    except Exception as e:
        current_app.logger.error(f"Error occurred: {e}")
        return jsonify({"error": "Erreur lors de l'enregistrement du Remplissage par défaut", "details": str(e)}), 500
