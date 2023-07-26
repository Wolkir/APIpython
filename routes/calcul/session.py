from flask import Flask, Blueprint, jsonify
from pymongo import MongoClient
from datetime import datetime

session = Blueprint('session', __name__)

# Connexion à la base de données MongoDB
#client = MongoClient('mongodb+srv://pierre:ztxiGZypi6BGDMSY@atlascluster.sbpp5xm.mongodb.net/?retryWrites=true&w=majority')
#db = client['test']
#collection = db['things']

#@session.route('/session', methods=['GET'])
def determine_session():
    data = request.json  # Récupérer les données JSON de la requête


    # Parcourir tous les documents pour déterminer la session en fonction de l'heure d'ouverture
    for doc in data:
        opening_time = doc['dateAndTimeOpening']

        # Déterminer la session en fonction de l'heure d'ouverture
        session = ""
        if opening_time.hour >= 0 and opening_time.hour < 7:
            session = "AS"
        elif opening_time.hour >= 8 and opening_time.hour < 12:
            session = "LD"
        elif opening_time.hour >= 13 and opening_time.hour < 15:
            session = "NY"
        else:
            session = "ND"

      

    return data['session']
