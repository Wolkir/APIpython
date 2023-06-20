from flask import Blueprint, jsonify
from pymongo import MongoClient
from bson import ObjectId
from datetime import datetime, timedelta
import json

dateDuJour = Blueprint('dateDuJour', __name__)

@dateDuJour.route('/datedujour', methods=['GET'])
def get_data_by_date():
    # Connexion à la base de données MongoDB
    client = MongoClient('mongodb+srv://pierre:ztxiGZypi6BGDMSY@atlascluster.sbpp5xm.mongodb.net/?retryWrites=true&w=majority')
    db = client['test']
    collection = db['things']

    # Récupération de la date actuelle
    current_date = datetime.now().date()

    # Calcul de la plage de dates pour la journée en cours
    start_date = datetime.combine(current_date, datetime.min.time())
    end_date = datetime.combine(current_date, datetime.max.time())

    # Requête pour récupérer les données dans la plage de dates spécifiée
    query = {
        "dateAndTimeOpening": {
            "$gte": start_date,
            "$lte": end_date
        }
    }
    data = list(collection.find(query))

    # Fermeture de la connexion à la base de données
    client.close()

    # Fonction de conversion personnalisée pour les objets ObjectId et datetime
    def serialize_object(obj):
        if isinstance(obj, ObjectId):
            return str(obj)
        elif isinstance(obj, datetime):
            return obj.isoformat()
        raise TypeError(f"Object of type {type(obj).__name__} is not JSON serializable")

    # Retourne les données au format JSON en utilisant la conversion personnalisée
    return jsonify(json.loads(json.dumps(data, default=serialize_object)))