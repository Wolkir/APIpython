from flask import Flask, Blueprint, jsonify, request
from pymongo import MongoClient
from bson import ObjectId
from datetime import datetime, timedelta
import json

# Connexion à la base de données MongoDB
client = MongoClient('mongodb+srv://pierre:ztxiGZypi6BGDMSY@atlascluster.sbpp5xm.mongodb.net/?retryWrites=true&w=majority')

slr = Blueprint('slr', __name__)

@slr.route('/slr', methods=['GET'])
def update_slr():
    # Connexion à la base de données MongoDB
    client = MongoClient('mongodb+srv://pierre:ztxiGZypi6BGDMSY@atlascluster.sbpp5xm.mongodb.net/?retryWrites=true&w=majority')
    db = client['test']
    collection = db['things']

    # Récupération des données de la collection things
    data = list(collection.find())

    # Parcours des données et mise à jour de la clé slr
    for entry in data:
        type_of_transaction = entry.get('typeOfTransaction')
        price_closure = entry.get('priceClosure')
        stopLoss = entry.get('stopLoss')

        print("type_of_transaction", type_of_transaction)
        print("price_closure:", price_closure)
        print("stopLoss:", stopLoss)

        if type_of_transaction == "buy" and price_closure <= stopLoss:
            entry['slr'] = True
        elif type_of_transaction == "sell" and price_closure >= stopLoss:
            entry['slr'] = True
        else:
            entry['slr'] = False

        print("slr:", entry['slr'])

        # Mise à jour du document dans la collection things
        collection.update_one({'_id': entry['_id']}, {'$set': {'slr': entry['slr']}})

    # Fermeture de la connexion à la base de données
    client.close()

    return jsonify({'message': 'slr updatedcsdc successfully'})