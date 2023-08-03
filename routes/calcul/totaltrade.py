from flask import Flask, Blueprint, jsonify
from pymongo import MongoClient
from datetime import timedelta

app = Flask(__name__)
totaltrade = Blueprint('totaltrade', __name__)

# Connexion à la base de données MongoDB
client = MongoClient('mongodb+srv://pierre:ztxiGZypi6BGDMSY@atlascluster.sbpp5xm.mongodb.net/?retryWrites=true&w=majority')
db = client['test']

@totaltrade.route('/totaltrade', methods=['GET'])
def calculate_totaltrade(data):

    username = data.get('username')
    collection_name = f"{username}_close"
    collection_unitaire = f"{username}_unitaire"
    collection = db[collection_name]

    # Obtenir tous les trades de la collection triés par ordre chronologique
    trades = collection.find().sort("timestamp", 1)

    # Numéro de position initialisé à 1
    position_number = 1

    # Parcourir chaque trade et lui attribuer un numéro de position
    for trade in trades:
        # Ajouter une nouvelle clé "totaltrade" au trade avec le numéro de position
        trade['totaltrade'] = position_number

        # Incrémenter le numéro de position pour le prochain trade
        position_number += 1

        # Mettre à jour le trade dans la collection MongoDB
        collection.update_one({'_id': trade['_id']}, {'$set': trade})

    return jsonify({'message': 'Numéro de position ajouté à chaque trade avec succès.'})

if __name__ == "__main__":
    app.run(debug=True)
