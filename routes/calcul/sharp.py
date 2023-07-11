from flask import Flask, Blueprint, jsonify
from pymongo import MongoClient
import numpy as np

sharp_ratio = Blueprint('sharp_ratio', __name__)

# Connexion à la base de données MongoDB
client = MongoClient('mongodb+srv://pierre:ztxiGZypi6BGDMSY@atlascluster.sbpp5xm.mongodb.net/?retryWrites=true&w=majority')
db = client['test']
collection = db['things']

@sharp_ratio.route('/sharp_ratio', methods=['GET'])
def calculate_sharp_ratio():
    # Récupérer tous les profits de la collection
    profits = [doc['profit'] for doc in collection.find()]

    # Calculer le ratio de Sharpe
    sharpe_ratio = np.mean(profits) / np.std(profits)

     # Insérer le winrate_value dans la collection "unitaire"
    unitaire_collection = db['unitaire']
    unitaire_collection.update_one({}, {"$set": {"sharpe": sharpe_ratio}}, upsert=True)

    return jsonify({"sharp_ratio": sharpe_ratio})