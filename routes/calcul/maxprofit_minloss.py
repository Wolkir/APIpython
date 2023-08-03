from flask import Flask, Blueprint, jsonify
from pymongo import MongoClient
import numpy as np

maxprofit_minloss = Blueprint('maxprofit_minloss', __name__)

# Connexion à la base de données MongoDB
client = MongoClient('mongodb+srv://pierre:ztxiGZypi6BGDMSY@atlascluster.sbpp5xm.mongodb.net/?retryWrites=true&w=majority')
db = client['test']


@maxprofit_minloss.route('/maxprofit_minloss', methods=['GET'])
def find_max_profit_and_min_loss(data):
    username = data.get('username')
    collection_name = f"{username}_close"
    collection_unitaire = f"{username}_unitaire"
    collection = db[collection_name]
    # Initialisation des variables
    max_profit_value = float('-inf')  # Valeur initiale de profit maximale
    min_loss_value = float('inf')  # Valeur initiale de perte minimale
    max_equity = None  # Initialiser la variable pour 'dd max'
    all_profits = []

    # Parcourir les documents de la collection
    for doc in collection.find():
        profit = doc['profit']
        all_profits.append(profit)

        # Recherche du profit maximum
        if profit > max_profit_value:
            max_profit_value = profit

        # Recherche de la perte minimale
        if profit < min_loss_value:
            min_loss_value = profit

        # Recherche de la valeur maximale de la perte ('dd max')
        equity = doc.get('Equity')
        if equity is not None and equity < 0:
            if max_equity is None or equity < max_equity:
                max_equity = equity

    # Convertir la liste en un tableau NumPy pour faciliter les calculs
    all_profits_arr = np.array(all_profits)

    # Calculer le ratio de Sharpe
    sharpe_ratio = np.mean(all_profits_arr) / np.std(all_profits_arr) if (np.std(all_profits_arr) > 0 else 0

    # Insérer les valeurs dans la collection "unitaire"
    unitaire_collection = db[collection_unitaire]
    unitaire_collection.update_one(
        {},
        {'$set': {'sharpe': sharpe_ratio, 'Max profit': max_profit_value, 'Max loss': min_loss_value, 'dd max': max_equity}},
        upsert=True
    )
