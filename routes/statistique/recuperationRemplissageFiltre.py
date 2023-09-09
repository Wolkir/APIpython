from flask import Blueprint, request, jsonify
from pymongo import MongoClient

recuperationRemplissageFiltre = Blueprint('recuperationRemplissageFiltre', __name__)

client = MongoClient('mongodb+srv://pierre:ztxiGZypi6BGDMSY@atlascluster.sbpp5xm.mongodb.net/?retryWrites=true&w=majority')
db = client['test']
collection = db['remplissageFiltre']

@recuperationRemplissageFiltre.route('/recuperationRemplissageFiltre', methods=['GET'])
def get_par_nom_remplissage():
    try:
        nom_remplissage = request.args.get('nomRemplissage', None)
        if not nom_remplissage:
            return jsonify({"message": "Le paramètre 'nomRemplissage' est requis"}), 400

        document = collection.find_one({"nomRemplissage": nom_remplissage}, {"_id": 0})

        if document:
            return jsonify(document), 200
        else:
            return jsonify({"message": "Aucune donnée trouvée pour le nomRemplissage spécifié"}), 404
    except Exception as e:
        return jsonify({"message": str(e)}), 500
