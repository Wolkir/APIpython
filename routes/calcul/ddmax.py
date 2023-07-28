from flask import Flask, Blueprint, jsonify
from pymongo import MongoClient

ddmax = Blueprint('ddmax', __name__)

# Connexion à la base de données MongoDB
client = MongoClient('mongodb+srv://pierre:ztxiGZypi6BGDMSY@atlascluster.sbpp5xm.mongodb.net/?retryWrites=true&w=majority')
db = client['test']



@ddmax.route('/ddmax', methods=['GET'])
def calculate_ddmax(data):
    username = data.get('username')
    collection_name = f"{username}_close"
    collection_unitaire = f"{username}_unitaire"
    collection = db[collection_name]
  
    # Requête pour trouver le montant négatif le plus grand
    pipeline = [
        {'$match': {'Equity': {'$lt': 0}}},
        {'$sort': {'Equity': 1}},
        {'$limit': 1}
    ]

    # Exécution de la requête
    result = list(collection.aggregate(pipeline))

    # Vérification du résultat
    max_equity = result[0]['Equity'] if result else None

    # Ajouter le résultat à la collection "unitaire"
    unitaire_collection = db[collection_unitaire]
    unitaire_collection.update_one({}, {'$set': {'dd max': (max_equity)}}, upsert=True)
 
