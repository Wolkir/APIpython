from flask import Flask, Blueprint, jsonify
from pymongo import MongoClient

winratestd = Blueprint('winratestd', __name__)

# Connexion à la base de données MongoDB
client = MongoClient('mongodb+srv://pierre:ztxiGZypi6BGDMSY@atlascluster.sbpp5xm.mongodb.net/?retryWrites=true&w=majority')
db = client['test']


@winrate.route('/winratestd', methods=['GET'])
def calculate_winratestd(data):
    username = data.get('username')
    identifier = data.get('identifier')
    collection_name = f"{username}_close"
    collection_unitaire = f"{username}_unitaire"
    collection = db[collection_name]
    # Compter le nombre de documents avec profit > 0
    positive_profits_count = collection.count_documents({"profit": {"$gt": 0}})
    
    # Compter le nombre de documents avec profit < 0
    negative_profits_count = collection.count_documents({"profit": {"$lt": 0}})
    
    # Calcul du winrate
    winratestd = positive_profits_count / (positive_profits_count + negative_profits_count) * 100
    
    #insérer le winrate_value dans la collection "unitaire"
    unitaire_collection = db[collection_unitaire]
    unitaire_collection.update_one({}, {'$set': {'winratestdl': (winratestd)}}, upsert=True)
