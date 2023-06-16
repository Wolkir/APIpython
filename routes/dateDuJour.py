from flask import Blueprint, jsonify
from pymongo import MongoClient
from bson import ObjectId
import json
from datetime import datetime

dateSeul = Blueprint('dateDuJour', __name__)

@dateSeul.route('/dateseul', methods=['GET'])
def get_data_by_date():
    # Connexion à la base de données MongoDB
    client = MongoClient('mongodb+srv://pierre:ztxiGZypi6BGDMSY@atlascluster.sbpp5xm.mongodb.net/?retryWrites=true&w=majority')
    db = client['test']
    collection = db['testDate']

    # Obtention de la date du jour
    date = datetime.now()

    # Requête pour récupérer les données par date
    query = {"date": date}
    data = list(collection.find(query))

    # Fermeture de la connexion à la base de données
    client.close()

    # Fonction de conversion personnalisée pour les objets ObjectId et datetime
    def serialize_object(obj):
        if isinstance(obj, (ObjectId, datetime)):
            return str(obj)
        raise TypeError(f"Object of type {type(obj).__name__} is not JSON serializable")

    # Retourne les données en format JSON en utilisant la conversion personnalisée
    return jsonify(json.loads(json.dumps(data, default=serialize_object)))

