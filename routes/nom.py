from flask import Blueprint, jsonify
from pymongo import MongoClient
from bson import ObjectId
import json

nom = Blueprint('nom', __name__)

@nom.route('/users', methods=['GET'])
def get_all_users():
    # Connexion à la base de données MongoDB
    client = MongoClient('mongodb+srv://pierre:ztxiGZypi6BGDMSY@atlascluster.sbpp5xm.mongodb.net/?retryWrites=true&w=majority')
    db = client['test']
    collection = db['testNom']

    # Récupération de toutes les données de la collection
    users = list(collection.find())

    # Fermeture de la connexion à la base de données
    client.close()

    # Fonction de conversion personnalisée pour les objets ObjectId
    def serialize_object_id(obj):
        if isinstance(obj, ObjectId):
            return str(obj)
        raise TypeError(f"Object of type {type(obj).__name__} is not JSON serializable")

    # Retourne les données en format JSON en utilisant la conversion personnalisée
    return jsonify(json.loads(json.dumps(users, default=serialize_object_id)))
