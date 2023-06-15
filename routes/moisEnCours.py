from flask import Blueprint, jsonify
from pymongo import MongoClient
from bson import ObjectId
from datetime import datetime, timedelta
import json

moisEnCours = Blueprint('moisEnCours', __name__)

@moisEnCours.route('/moisencours', methods=['GET'])
def get_data_by_month():
    # Connexion à la base de données MongoDB
    client = MongoClient('mongodb+srv://pierre:ztxiGZypi6BGDMSY@atlascluster.sbpp5xm.mongodb.net/?retryWrites=true&w=majority')
    db = client['test']
    collection = db['testDate']

    # Récupération de la date actuelle
    current_date = datetime.now()

    # Calcul de la première journée du mois actuel
    start_date = datetime(current_date.year, current_date.month, 1)

    # Calcul de la dernière journée du mois actuel
    next_month = current_date.replace(day=28) + timedelta(days=4)  # Ajout de 4 jours pour prendre en compte les mois de 30 ou 31 jours
    end_date = next_month - timedelta(days=next_month.day)

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

    # Fonction de conversion personnalisée pour les objets ObjectId et datetime
    def serialize_object(obj):
        if isinstance(obj, ObjectId):
            return str(obj)
        elif isinstance(obj, datetime):
            return obj.isoformat()
        raise TypeError(f"Object of type {type(obj).__name__} is not JSON serializable")

    # Retourne les données au format JSON en utilisant la conversion personnalisée
    return jsonify(json.loads(json.dumps(data, default=serialize_object)))
