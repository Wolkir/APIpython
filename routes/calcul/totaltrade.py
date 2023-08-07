from flask import Flask, Blueprint, jsonify
from pymongo import MongoClient
from datetime import timedelta
from bson import ObjectId


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

    # Compter le nombre total de trades dans la collection
    total_trades = collection.count_documents({})

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

    # Si la collection est vide, il n'y a pas de trade à numéroté
    if total_trades == 0:
        return jsonify({'message': 'Aucun trade à numéroter.'})

    # Ajouter le numéro de position pour le dernier trade ajouté à la collection
    last_trade = collection.find_one(sort=[('timestamp', -1)])
    last_trade['totaltrade'] = total_trades
    collection.update_one({'_id': last_trade['_id']}, {'$set': last_trade})

    first_trade = collection.find_one(sort=[('timestamp', 1)])
    if first_trade:
        collection.update_one({'_id': first_trade['_id']}, {'$set': {'totaltrade': 1}})

    last_trade['_id'] = ObjectId()  # Générer un nouvel ID pour éviter des doublons
    last_trade['total_trade'] = total_trades
    unitaire_collection.insert_one(last_trade)

    return jsonify({'message': 'Numéro de position ajouté à chaque trade avec succès.'})

if __name__ == "__main__":
    app.run(debug=True)
