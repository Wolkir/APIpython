from flask import Flask, Blueprint, jsonify, request
from pymongo import MongoClient
from datetime import datetime

tradecount = Blueprint('tradecount', __name__)

# Connexion à la base de données MongoDB
client = MongoClient('mongodb+srv://pierre:ztxiGZypi6BGDMSY@atlascluster.sbpp5xm.mongodb.net/?retryWrites=true&w=majority')
db = client['test']

@tradecount.route('/tradecount', methods=['POST'])
def calculate_tradecount():
    
    data = request.json
    username = data.get('username')
    # Récupérer la date sans l'heure, les minutes et les secondes
    date_of_trade = datetime.strptime(data.get('date'), '%Y-%m-%dT%H:%M:%S.%f%z').strftime('%Y-%m-%d')
    
    collection_close = db[f"{username}_close"]
    collection_open = db[f"{username}_open"]

    # Comptez les trades fermés et ouverts pour la date donnée
    count_close = collection_close.count_documents({"date": {"$regex": f"^{date_of_trade}"}})
    count_open = collection_open.count_documents({"date": {"$regex": f"^{date_of_trade}"}})

    # Calculer le numéro de trade pour le nouveau trade
    new_trade_number = count_close + count_open + 1

    # À ce stade, vous pouvez soit ajouter ce nouveau trade à la collection appropriée, soit renvoyer ce numéro.
    # Note: Si vous l'ajoutez à la collection, assurez-vous d'inclure le numéro dans le document de trade.

    return new_trade_number

