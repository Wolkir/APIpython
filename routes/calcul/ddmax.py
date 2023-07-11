from flask import Flask, Blueprint, jsonify
from pymongo import MongoClient

ddmax = Blueprint('ddmax', __name__)

# Connexion à la base de données MongoDB
client = MongoClient('mongodb+srv://pierre:ztxiGZypi6BGDMSY@atlascluster.sbpp5xm.mongodb.net/?retryWrites=true&w=majority')
db = client['test']
collection = db['things']
unitaire_collection = db['unitaire']

@ddmax.route('/ddmax', methods=['GET'])
def calculate_ddmax():
    # Requête pour trouver le montant négatif le plus grand
    pipeline = [
        {'$match': {'equity': {'$lt': 0}}},
        {'$sort': {'equity': 1}},
        {'$limit': 1}
    ]

    # Exécution de la requête
    result = list(collection.aggregate(pipeline))

    # Vérification du résultat
    max_equity = result[0]['equity'] if result else None

    # Ajouter le résultat à la collection "unitaire"
    unitaire_collection.update_one({}, {'$set': {'ddmax': max_equity}}, upsert=True)

    return jsonify({"ddmax": max_equity})