from flask import Flask, Blueprint, jsonify
from pymongo import MongoClient
from datetime import timedelta

app = Flask(__name__)
totaltrade = Blueprint('totaltrade', __name__)

# Connexion à la base de données MongoDB
client = MongoClient('mongodb+srv://pierre:ztxiGZypi6BGDMSY@atlascluster.sbpp5xm.mongodb.net/?retryWrites=true&w=majority')
db = client['test']


@totaltrade.route('/totaltrade', methods=['GET'])
def calculate_totaltrade():
    username = "Trader"  # Remplacez ceci par le nom d'utilisateur approprié

    collection_name = f"{username}_close"
    collection_unitaire = f"{username}_unitaire"
    collection = db[collection_name]

    # Vérifiez si l'utilisateur a déjà un trade dans la collection
    has_trades = collection.count_documents({}) > 0

    if has_trades:
        # Si l'utilisateur a déjà des trades, récupérez le dernier trade sans mise à jour
        last_trade = collection.find_one(sort=[('timestamp', -1)])
        total_trades = last_trade.get('totaltrade', 0)
    else:
        # Si l'utilisateur n'a pas de trade, initialisez totaltrade à 1
        total_trades = 1
        # Insérez le premier trade avec totaltrade à 1
        current_timestamp = datetime.now()
        first_trade = {
            'totaltrade': total_trades,
            'timestamp': current_timestamp
            # Les autres détails du premier trade ici
        }
        collection.insert_one(first_trade)

    # Ajouter 1 pour le nouveau trade seulement si l'utilisateur a déjà des trades
    if has_trades:
        total_trades += 1

    # Insérer le nouveau trade dans la collection avec le bon totaltrade
    current_timestamp = datetime.now()
    new_trade = {
        'totaltrade': total_trades,
        'timestamp': current_timestamp
        # Les autres détails du nouveau trade ici
    }
    collection.insert_one(new_trade)
