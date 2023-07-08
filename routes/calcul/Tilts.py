from flask import Flask, Blueprint, jsonify, request
from pymongo import MongoClient
from bson import ObjectId
from datetime import datetime, timedelta
import json

# Connexion à la base de données MongoDB
client = MongoClient('mongodb+srv://pierre:ztxiGZypi6BGDMSY@atlascluster.sbpp5xm.mongodb.net/?retryWrites=true&w=majority')

Tilts = Blueprint('Tilts', __name__)

@Tilts.route('/Tilts', methods=['GET'])
def update_Tilts():
    # Connexion à la base de données MongoDB
    client = MongoClient('mongodb+srv://pierre:ztxiGZypi6BGDMSY@atlascluster.sbpp5xm.mongodb.net/?retryWrites=true&w=majority')
    db = client['test']
    collection = db['thingsTest']
    perte_journaliere_collection = db['perteJournaliere']

    # Récupération des données de la collection things
    data = list(collection.find({'profit': {'$lt': 0}}))

    # Parcours des données et enregistrement dans la collection perteJournaliere
    for entry in data:
        # Ajout des données dans la collection perteJournaliere
        perte_journaliere_collection.insert_one(entry)

    # Fermeture de la connexion à la base de données
    client.close()

    return jsonify({'message': 'Data with negative profit saved in perteJournaliere collection'})
