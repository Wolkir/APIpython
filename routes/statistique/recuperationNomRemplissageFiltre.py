from flask import Blueprint, request, jsonify
from pymongo import MongoClient

recuperationNomRemplissageFiltre = Blueprint('recuperationNomRemplissageFiltre', __name__)

# Initialisez la connexion à la base de données MongoDB
client = MongoClient('mongodb+srv://pierre:ztxiGZypi6BGDMSY@atlascluster.sbpp5xm.mongodb.net/?retryWrites=true&w=majority')
db = client['test']
collection = db['remplissageFiltre']

@recuperationNomRemplissageFiltre.route('/recuperationNomRemplissageFiltre', methods=['GET'])
def get_nom_remplissage():
    try:
        username = request.args.get('username', None)
        if not username:
            return jsonify({"message": "Le paramètre 'username' est requis"}), 400

        # Rechercher les documents avec le champ 'username' égal à la valeur fournie
        cursor = collection.find({"username": username}, {"_id": 0, "nomRemplissage": 1})

        # Extraire les valeurs du champ 'nomRemplissage' dans une liste
        nom_remplissage_list = [doc["nomRemplissage"] for doc in cursor]

        return jsonify({"nomRemplissage": nom_remplissage_list}), 200
    except Exception as e:
        return jsonify({"message": str(e)}), 500
