from flask import Flask, Blueprint, jsonify
from pymongo import MongoClient

winrate = Blueprint('winrate', __name__)

# Connexion à la base de données MongoDB
client = MongoClient('mongodb+srv://pierre:ztxiGZypi6BGDMSY@atlascluster.sbpp5xm.mongodb.net/?retryWrites=true&w=majority')
db = client['collection']


@winrate.route('/winrate', methods=['GET'])
def calculate_winrate(data):
    username = data.get('username')
    collection_name = f"{username}_close"
    collection_unitaire = f"{username}_unitaire"
    collection = db[collection_name]
  
    # Compter le nombre de documents avec profit > 0
    positive_profits_count = collection.count_documents({"profit": {"$gt": 0}})
    
    # Compter le nombre de documents avec profit < 0
    negative_profits_count = collection.count_documents({"profit": {"$lt": 0}})
    
    # Calcul du winrate
    winrate = (positive_profits_count / (positive_profits_count + negative_profits_count)) * 100
    
    # Insérer le winrate_value dans la collection "unitaire"
    unitaire_collection = db[collection_unitaire]
    unitaire_collection.update_one({}, {'$set': {'winratestd': (winrate)}}, upsert=True)
