from flask import Blueprint, jsonify
from pymongo import MongoClient
from bson import ObjectId
from datetime import datetime, timedelta
import json

moisGlissant = Blueprint('moisGlissant', __name__)

@moisGlissant.route('/moisglissant', methods=['GET'])
def get_data_with_conditions():
    # Connexion à la base de données MongoDB
    client = MongoClient('mongodb+srv://pierre:ztxiGZypi6BGDMSY@atlascluster.sbpp5xm.mongodb.net/?retryWrites=true&w=majority')
    db = client['test']
    collection = db['testDate']

    # Définition de la valeur pour la première condition (date d'aujourd'hui)
    valeur_1 = datetime.now()

    # Calcul de la valeur pour la deuxième condition (1 mois plus tard que la date d'aujourd'hui)
    valeur_2 = valeur_1 + timedelta(days=30)

    # Requête pour récupérer les données dans la plage de dates spécifiée
    query = {
        "date": {
            "$gte": valeur_1,
            "$lte": valeur_2
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
