from flask import Flask, Blueprint, jsonify
from pymongo import MongoClient

winrate = Blueprint('winrate', __name__)

# Connexion à la base de données MongoDB
client = MongoClient('mongodb+srv://pierre:ztxiGZypi6BGDMSY@atlascluster.sbpp5xm.mongodb.net/?retryWrites=true&w=majority')
db = client['test']


@winrate.route('/winrate', methods=['GET'])
def calculate_winrate():
    data = request.json
    username = data.get('username')
    identifier = data.get('identifier')
    collection_name = data.get('collection')
    collection_unitaire = f"{username}_unitaire"
    collection = db[collection_name]
  
    # Récupérer tous les documents
    documents = list(collection.find())
    
    positive_profits_count = 0
    negative_profits_count = 0
    
    positive_identifiers = set()
    negative_identifiers = set()
    
    for doc in documents:
        profit = doc['profit']
        identifier = doc['identifier']
        
        if profit > 0 and identifier not in positive_identifiers:
            positive_profits_count += 1
            positive_identifiers.add(identifier)
        elif profit < 0 and identifier not in negative_identifiers:
            negative_profits_count += 1
            negative_identifiers.add(identifier)

    
    # Calcul du winrate
    winrate_value = positive_profits_count / (positive_profits_count + negative_profits_count) * 100
    
    # Insérer le winrate_value dans la collection "unitaire"
    unitaire_collection = db[collection_unitaire]
    unitaire_collection.update_one({}, {'$set': {'winratereal': (winrate_value)}}, upsert=True)
