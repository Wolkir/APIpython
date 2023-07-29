from flask import Flask, Blueprint, jsonify
from pymongo import MongoClient

max_successive_losses = Blueprint('max_successive_losses', __name__)

# Connexion à la base de données MongoDB
client = MongoClient('mongodb+srv://pierre:ztxiGZypi6BGDMSY@atlascluster.sbpp5xm.mongodb.net/?retryWrites=true&w=majority')
db = client['test']


@max_successive_losses.route('/max_successive_losses', methods=['GET'])
def find_max_successive_losses(data):
    username = data.get('username')
    collection_name = f"{username}_close"
    collection_unitaire = f"{username}_unitaire"
    collection = db[collection_name]
    # Initialisation des variables
    max_successive_losses_count = 0
    current_successive_losses_count = 0
    previous_identifier = None

    # Initialisation des variables
    max_successive_losses_count = 0
    current_successive_losses_count = 0

    # Parcourir les documents de la collection
    for doc in collection.find().sort("identifier"):
        profit = doc['profit']

        if profit < 0:
            current_successive_losses_count += 1
        else:
            # Réinitialiser le compteur si on trouve un profit positif
            if current_successive_losses_count > max_successive_losses_count:
                max_successive_losses_count = current_successive_losses_count
            current_successive_losses_count = 0

    # Vérifier le compteur à la fin de la boucle
    if current_successive_losses_count > max_successive_losses_count:
        max_successive_losses_count = current_successive_losses_count

    # Insérer le max_successive_loss dans la collection "unitaire"
    unitaire_collection = db[collection_unitaire]
    unitaire_collection.update_one({}, {'$set': {'max_successive_loss': max_successive_losses_count}}, upsert=True)
