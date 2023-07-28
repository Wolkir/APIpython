from flask import Flask, Blueprint, jsonify
from pymongo import MongoClient

maxprofit = Blueprint('maxprofit', __name__)

# Connexion à la base de données MongoDB
client = MongoClient('mongodb+srv://pierre:ztxiGZypi6BGDMSY@atlascluster.sbpp5xm.mongodb.net/?retryWrites=true&w=majority')
db = client['test']

@maxprofit.route('/maxprofit', methods=['GET'])
def find_max_profit(data):
    username = data.get('username')
    collection_name = f"{username}_close"
    collection_unitaire = f"{username}_unitaire"
    collection = db[collection_name]
    # Recherche de la ligne avec le profit > 0 le plus grand
    max_profit = collection.find_one({"profit": {"$gt": 0}}, sort=[("profit", -1)])

    if max_profit:
        profit_value = max_profit['profit']
        
        unitaire_collection = db[collection_unitaire]
        unitaire_collection.update_one({}, {'$set': {'Max profit': (profit_value)}}, upsert=True)
