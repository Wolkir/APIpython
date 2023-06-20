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
    collection = db['things']

    # Calcul de la date de début (7 jours avant la date d'aujourd'hui)
    start_date = datetime.now() - timedelta(days=7)

    # Calcul de la date de fin (la date d'aujourd'hui)
    end_date = datetime.now()

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
        if isinstance(obj, (ObjectId, datetime)):
            return str(obj)
        raise TypeError(f"Object of type {type(obj).__name__} is not JSON serializable")

    # Retourne les données au format JSON en utilisant la conversion personnalisée
    return jsonify(json.loads(json.dumps(data, default=serialize_object)))
