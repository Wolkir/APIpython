from flask import Flask, Blueprint, jsonify, request
from pymongo import MongoClient
from bson import ObjectId
from datetime import datetime, timedelta
import json

# Connexion à la base de données MongoDB
client = MongoClient('mongodb+srv://pierre:ztxiGZypi6BGDMSY@atlascluster.sbpp5xm.mongodb.net/?retryWrites=true&w=majority')

tpr = Blueprint('tpr', __name__)

@tpr.route('/tpr', methods=['GET'])
def update_tpr():
    # Connexion à la base de données MongoDB
    client = MongoClient('mongodb+srv://pierre:ztxiGZypi6BGDMSY@atlascluster.sbpp5xm.mongodb.net/?retryWrites=true&w=majority')
    db = client['test']
    collection = db['things']

    # Récupération des données de la collection things
    data = list(collection.find())

    # Parcours des données et mise à jour de la clé TPR
    for entry in data:
        type_of_transaction = entry.get('typeOfTransaction')
        price_closure = entry.get('priceClosure')
        take_profit = entry.get('takeProfit')

        print("type_of_transaction", type_of_transaction)
        print("price_closure:", price_closure)
        print("take_profit:", take_profit)

        if type_of_transaction == "buy" and price_closure >= take_profit:
            entry['TPR'] = True
        elif type_of_transaction == "sell" and price_closure <= take_profit:
            entry['TPR'] = True
        else:
            entry['TPR'] = False

        print("TPR:", entry['TPR'])

        # Mise à jour du document dans la collection things
        collection.update_one({'_id': entry['_id']}, {'$set': {'TPR': entry['TPR']}})

    # Fermeture de la connexion à la base de données
    client.close()

    return jsonify({'message': 'TPR updatedcsdc successfully'})