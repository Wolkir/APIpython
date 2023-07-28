from flask import Flask, Blueprint, jsonify
from pymongo import MongoClient

profitfactorlong = Blueprint('profitfactorlong', __name__)

# Connexion à la base de données MongoDB
client = MongoClient('mongodb+srv://pierre:ztxiGZypi6BGDMSY@atlascluster.sbpp5xm.mongodb.net/?retryWrites=true&w=majority')
db = client['test']


@profitfactorlong.route('/profitfactorlong', methods=['GET'])
def calculate_profit_factor_long(data):
    username = data.get('username')
    collection_name = f"{username}_close"
    collection_unitaire = f"{username}_unitaire"
    collection = db[collection_name]
    # Calcul du profit total et de la perte totale pour les transactions de type "buy"
    total_profit = 0
    total_loss = 0

    # Parcourir les documents de la collection
    for doc in collection.find({"typeOfTransaction": "buy"}):
        profit = doc['profit']
        if profit > 0:
            total_profit += profit
        elif profit < 0:
            total_loss += profit

    print(f"Total du profit : {total_profit}")
    print(f"Total de la perte : {total_loss}")

    # Calcul du profit factor
    profit_factor = total_profit / abs(total_loss)

   # Insérer le winrate_value dans la collection "unitaire"
    unitaire_collection = db[collection_name]
    unitaire_collection.update_one({}, {'$set': {'profitfactorlong': (profit_factor)}}, upsert=True)
    unitaire_collection.update_one({}, {'$set': {'total loss long': (total_loss)}}, upsert=True)
    unitaire_collection.update_one({}, {'$set': {'total gain long': (total_gain)}}, upsert=True)
