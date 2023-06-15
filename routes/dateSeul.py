from flask import Blueprint, jsonify
from pymongo import MongoClient
from bson import ObjectId
import json
from datetime import datetime

dateSeul = Blueprint('dateSeul', __name__)

@dateSeul.route('/dateseul', methods=['GET'])
def get_data_by_date():
    # Connexion à la base de données MongoDB
    client = MongoClient('mongodb+srv://pierre:ztxiGZypi6BGDMSY@atlascluster.sbpp5xm.mongodb.net/?retryWrites=true&w=majority')
    db = client['test']
    collection = db['testDate']

    # Convertir la chaîne de date en objet datetime
    date_str = "2023-11-30T00:00:00.000+00:00"
    date = datetime.fromisoformat(date_str)

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
