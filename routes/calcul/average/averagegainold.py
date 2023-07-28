from flask import Flask, Blueprint, jsonify
from pymongo import MongoClient

averagegain = Blueprint('averagegain', __name__)

# Connexion à la base de données MongoDB
client = MongoClient('mongodb+srv://pierre:ztxiGZypi6BGDMSY@atlascluster.sbpp5xm.mongodb.net/?retryWrites=true&w=majority')
db = client['test']
collection = db['things']

@averagegain.route('/averagegain', methods=['GET'])
def calculate_average_gain():
    # Initialisation des variables
    positive_gains_total = 0
    positive_gains_count = 0
    positive_ticket_numbers = set()

    # Parcourir les documents de la collection
    for doc in collection.find():
        profit = doc['profit']
        ticket_number = doc['ticketNumber']
        
        if profit > 0 and ticket_number not in positive_ticket_numbers:
            positive_gains_total += profit
            positive_gains_count += 1
            positive_ticket_numbers.add(ticket_number)

    # Calcul de la moyenne des gains
    average_gain = positive_gains_total / positive_gains_count if positive_gains_count > 0 else 0

    # Insérer le winrate_value dans la collection "unitaire"
    unitaire_collection = db['unitaire']
    unitaire_collection.insert_one({"averagegain": average_gain})

    return jsonify({"average_gain": average_gain})
