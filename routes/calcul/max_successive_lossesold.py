from flask import Flask, Blueprint, jsonify
from pymongo import MongoClient

max_successive_losses = Blueprint('max_successive_losses', __name__)

# Connexion à la base de données MongoDB
client = MongoClient('mongodb+srv://pierre:ztxiGZypi6BGDMSY@atlascluster.sbpp5xm.mongodb.net/?retryWrites=true&w=majority')
db = client['test']
collection = db['things']

@max_successive_losses.route('/max_successive_losses', methods=['GET'])
def find_max_successive_losses():
    # Initialisation des variables
    max_successive_losses_count = 0
    current_successive_losses_count = 0
    previous_ticket_number = None

    # Parcourir les documents de la collection
    for doc in collection.find().sort("ticketNumber"):
        profit = doc['profit']
        ticket_number = doc['ticketNumber']

        if profit < 0:
            if ticket_number != previous_ticket_number:
                current_successive_losses_count = 1
            else:
                current_successive_losses_count += 1

            if current_successive_losses_count > max_successive_losses_count:
                max_successive_losses_count = current_successive_losses_count

        previous_ticket_number = ticket_number

    return jsonify({"max_successive_losses": max_successive_losses_count})
