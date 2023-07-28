from flask import Flask, Blueprint, jsonify
from pymongo import MongoClient

averageloss = Blueprint('averageloss', __name__)

# Connexion à la base de données MongoDB
client = MongoClient('mongodb+srv://pierre:ztxiGZypi6BGDMSY@atlascluster.sbpp5xm.mongodb.net/?retryWrites=true&w=majority')
db = client['test']


@averageloss.route('/averageloss', methods=['GET'])
def calculate_average_loss(data):
    username = data.get('username')
    collection_name = f"{username}_close"
    collection_unitaire = f"{username}_unitaire"
  
    collection = db[collection_name]
    # Initialisation des variables
    negative_losses_total = 0
    negative_losses_count = 0
    negative_ticket_numbers = set()

    # Parcourir les documents de la collection
    for doc in collection.find():
        profit = doc['profit']
        ticket_number = doc['ticketNumber']
        
        if profit < 0 and ticket_number not in negative_ticket_numbers:
            negative_losses_total += profit
            negative_losses_count += 1
            negative_ticket_numbers.add(ticket_number)

    # Calcul de la moyenne des pertes
    average_loss = negative_losses_total / negative_losses_count if negative_losses_count > 0 else 0
    unitaire_collection = db[collection_unitaire]
    unitaire_collection.insert_one({"averageloss": average_loss})


