from flask import Blueprint, jsonify
from pymongo import MongoClient
from bson import ObjectId
from datetime import datetime, timedelta
import json

semaineGlissante = Blueprint('semaineGlissante', __name__)

@semaineGlissante.route('/semaineglissante', methods=['GET'])
def get_data_by_date():
    # Connexion à la base de données MongoDB
    client = MongoClient('mongodb+srv://pierre:ztxiGZypi6BGDMSY@atlascluster.sbpp5xm.mongodb.net/?retryWrites=true&w=majority')
    db = client['test']
    collection = db['testDate']

    # Définition de la date de départ
    start_date_str = "2023-06-07T10:55:04.000+00:00"
    start_date = datetime.fromisoformat(start_date_str)

    # Calcul de la date 7 jours plus tard
    end_date = start_date + timedelta(days=7)

    # Requête pour récupérer les données dans la plage de dates spécifiée
    query = {
        "date": {
            "$gte": start_date,
            "$lte": end_date
        }
    }
    data = list(collection.find(query))

    # Fermeture de la connexion à la base de données
    client.close()

    # Fonction de conversion personnalisée pour les objets ObjectId
    # Fonction de conversion personnalisée pour les objets ObjectId et datetime
    def serialize_object_id(obj):
        if isinstance(obj, ObjectId):
            return str(obj)
        elif isinstance(obj, datetime):
            return obj.isoformat()
        raise TypeError(f"Object of type {type(obj).__name__} is not JSON serializable")


    # Retourne les données en format JSON en utilisant la conversion personnalisée
    return jsonify(json.loads(json.dumps(data, default=serialize_object_id)))
