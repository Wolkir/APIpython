from flask import Flask, Blueprint, jsonify
from pymongo import MongoClient
from datetime import datetime, time

# Connexion à la base de données MongoDB
client = MongoClient('mongodb+srv://pierre:ztxiGZypi6BGDMSY@atlascluster.sbpp5xm.mongodb.net/?retryWrites=true&w=majority')

killzone = Blueprint('killzone', __name__)

@killzone.route('/killzone', methods=['GET'])
def determine_killzone():
    # Parcourir tous les documents de la collection
    for doc in collection.find():
        # Récupérer l'heure d'ouverture de chaque document
        opening_time = doc['dateAndTimeOpening'].time()

        # Déterminer si l'heure d'ouverture se trouve dans l'une des plages horaires spécifiées
        if (time(3, 0) <= opening_time <= time(6, 0)) or (time(9, 0) <= opening_time <= time(12, 0)) or (time(14, 0) <= opening_time <= time(17, 0)):
            killzone = True
        else:
            killzone = False
            
    return entry

