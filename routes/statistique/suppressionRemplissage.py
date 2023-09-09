from flask import Blueprint, request, jsonify
from pymongo import MongoClient

suppressionRemplissage = Blueprint('suppressionRemplissage', __name__)

client = MongoClient('mongodb+srv://pierre:ztxiGZypi6BGDMSY@atlascluster.sbpp5xm.mongodb.net/?retryWrites=true&w=majority')
db = client['test']
collection = db['remplissageFiltre']

@suppressionRemplissage.route('/suppressionRemplissage', methods=['DELETE'])
def delete_remplissage_filtre():
    try:
        nomRemplissage = request.args.get('nomRemplissage', None)

        if nomRemplissage is None:
            return jsonify({"message": "L'argument 'nomRemplissage' est requis"}), 400

        # Supprimer le document avec le champ nomRemplissage égal à l'argument nomRemplissage
        result = collection.delete_many({"nomRemplissage": nomRemplissage})

        if result.deleted_count > 0:
            return jsonify({"message": f"{result.deleted_count} documents supprimés avec succès"}), 200
        else:
            return jsonify({"message": f"Aucun document avec nomRemplissage='{nomRemplissage}' trouvé"}), 404
    except Exception as e:
        return jsonify({"message": str(e)}), 500
