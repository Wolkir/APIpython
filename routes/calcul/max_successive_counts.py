from flask import Flask, Blueprint, jsonify
from pymongo import MongoClient

max_successive_counts = Blueprint('max_successive_counts', __name__)

# Connexion à la base de données MongoDB
client = MongoClient('mongodb+srv://pierre:ztxiGZypi6BGDMSY@atlascluster.sbpp5xm.mongodb.net/?retryWrites=true&w=majority')
db = client['test']


@max_successive_counts.route('/max_successive_counts', methods=['GET'])
def find_max_successive_counts(data):
    username = data.get('username')
    collection_name = f"{username}_close"
    collection_unitaire = f"{username}_unitaire"
    collection = db[collection_name]
    # Initialisation des variables
    max_successive_gains_count = 0
    max_successive_losses_count = 0
    current_successive_gains_count = 0
    current_successive_losses_count = 0
    previous_identifier = None

    # Parcourir les documents de la collection
    for doc in collection.find().sort("identifier"):
        profit = doc['profit']

        # Gains successifs
        if profit > 0:
            current_successive_gains_count += 1
            # Réinitialiser le compteur de pertes si on trouve un gain
            current_successive_losses_count = 0
            # Mettre à jour le compteur de gains maximum
            if current_successive_gains_count > max_successive_gains_count:
                max_successive_gains_count = current_successive_gains_count
        # Pertes successives
        else:
            current_successive_losses_count += 1
            # Réinitialiser le compteur de gains si on trouve une perte
            current_successive_gains_count = 0
            # Mettre à jour le compteur de pertes maximum
            if current_successive_losses_count > max_successive_losses_count:
                max_successive_losses_count = current_successive_losses_count

    # Vérifier les compteurs à la fin de la boucle
    if current_successive_gains_count > max_successive_gains_count:
        max_successive_gains_count = current_successive_gains_count
    if current_successive_losses_count > max_successive_losses_count:
        max_successive_losses_count = current_successive_losses_count

    # Insérer les max_successive_gain et max_successive_loss dans la collection "unitaire"
    unitaire_collection = db[collection_unitaire]
    unitaire_collection.update_one(
        {},
        {'$set': {'max_successive_gain2': max_successive_gains_count, 'max_successive_loss2': max_successive_losses_count}},
        upsert=True
    )
