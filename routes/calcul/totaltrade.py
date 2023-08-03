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

    # Obtenir le dernier trade de la collection triée par ordre chronologique
    last_trade = collection.find_one(sort=[('timestamp', -1)])

    if last_trade is None:
        # Aucun trade dans la collection, le numéro de position sera 1
        total_trades = 1
    else:
        # Récupérer la valeur de totaltrade du dernier trade et ajouter 1 pour le nouveau trade
        total_trades = last_trade.get('totaltrade', 0) + 1

        # Mettre à jour le dernier trade avec le nouveau numéro de position "totaltrade"
        collection.update_one({'_id': last_trade['_id']}, {'$set': {'totaltrade': total_trades}})

    return jsonify({'totaltrade': total_trades})

if __name__ == "__main__":
    app.run(debug=True)

