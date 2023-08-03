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

    # Compter le nombre total de trades dans la collection
    total_trades = collection.count_documents({})

    if total_trades > 0:
        # Obtenir le dernier trade de la collection triée par ordre chronologique
        last_trade = collection.find_one(sort=[('timestamp', -1)])
        # Récupérer la valeur de totaltrade du dernier trade et ajouter 1 pour le nouveau trade
        total_trades = last_trade.get('totaltrade', 0) + 1

        # Ajouter le numéro de position pour le dernier trade ajouté à la collection
        last_trade['totaltrade'] = total_trades
        collection.update_one({'_id': last_trade['_id']}, {'$set': last_trade})

    return jsonify({'message': 'Numéro de position ajouté à chaque trade avec succès.'})

if __name__ == "__main__":
    app.run(debug=True)
