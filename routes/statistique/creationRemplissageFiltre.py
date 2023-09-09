from flask import Blueprint, request, jsonify, Flask
from pymongo import MongoClient

app = Flask(__name__)

creationRemplissageFiltre = Blueprint('creationRemplissageFiltre', __name__)

app.config['MONGO_URI'] = 'mongodb+srv://pierre:ztxiGZypi6BGDMSY@atlascluster.sbpp5xm.mongodb.net/?retryWrites=true&w=majority'
mongo = MongoClient(app.config['MONGO_URI'])
db = mongo["test"]
collection = db['remplissageFiltre']

@creationRemplissageFiltre.route('/creationRemplissageFiltre', methods=['POST'])
def creation_remplissage_filtre():
    try:
        tableau_json = request.get_json()
        if isinstance(tableau_json, list):
            # Créez un document MongoDB unique qui contient tous les sous-tableaux
            document_mongodb = {}
            for item in tableau_json:
                for key, value in item.items():
                    if key not in document_mongodb:
                        document_mongodb[key] = []
                    document_mongodb[key].append(value)

            # Insérez le document MongoDB unique dans la collection MongoDB
            collection.insert_one(document_mongodb)
            
            return jsonify({"message": "Données insérées avec succès"}), 200
        else:
            return jsonify({"message": "Le corps de la requête doit être un tableau JSON"}), 400
    except Exception as e:
        return jsonify({"message": str(e)}), 500
