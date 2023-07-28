from flask import Flask, Blueprint, jsonify
from pymongo import MongoClient

app = Flask(__name__)
profitfactor = Blueprint('profitfactor', __name__)

# Connexion à la base de données MongoDB
client = MongoClient('mongodb+srv://pierre:ztxiGZypi6BGDMSY@atlascluster.sbpp5xm.mongodb.net/?retryWrites=true&w=majority')
db = client['test']


@profitfactor.route('/profitfactor', methods=['GET'])
def calculate_profit_factor(data):
    username = data.get('username')
    collection_name = f"{username}_close"
    collection_unitaire = f"{username}_unitaire"
    collection = db[collection_name]

    
    # Calcul du profit total et du perte total
    total_profit = 0
    total_loss = 0

    # Parcourir les documents de la collection
    for doc in collection.find():
        profit = doc['profit']
        if profit > 0:
            total_profit += profit
        elif profit < 0:
            total_loss += profit
  
    # Calcul du profit factor
    profit_factor = total_profit / abs(total_loss)

    # Insérer le winrate_value dans la collection "unitaire"
    unitaire_collection = db[collection_unitaire]
    unitaire_collection.update_one({}, {'$set': {'profitfactor': (profit_factor)}}, upsert=True)
    unitaire_collection.update_one({}, {'$set': {'total loss': (total_loss)}}, upsert=True)
    unitaire_collection.update_one({}, {'$set': {'total gain': (total_gain)}}, upsert=True)
