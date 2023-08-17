from flask import Flask, Blueprint, jsonify
from pymongo import MongoClient
import numpy as np

# Connexion à la base de données MongoDB
client = MongoClient('mongodb+srv://pierre:ztxiGZypi6BGDMSY@atlascluster.sbpp5xm.mongodb.net/?retryWrites=true&w=majority')
db = client['test']
sharp = Blueprint('sharp', __name__)

@sharp.route('/sharp', methods=['GET'])
def calculate_sharp_ratio(data):
    username = data.get('username')
    collection_name = f"{username}_close"
    collection_unitaire = f"{username}_unitaire"
    collection = db[collection_name]

    # Récupérer tous les profits de la collection
    profits = [doc['profit'] for doc in collection.find()]

    # Calculer le ratio de Sharpe
    sharpe_ratio = np.mean(profits) / np.std(profits) if np.std(profits) > 0 else 0


     # Insérer le winrate_value dans la collection "unitaire"
    unitaire_collection = db[collection_unitaire]
    unitaire_collection.update_one({}, {"$set": {"sharpe": sharpe_ratio}}, upsert=True)
