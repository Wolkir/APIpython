from flask import Flask, Blueprint, jsonify
from pymongo import MongoClient
from datetime import timedelta, datetime

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

    if last_trade:
        # Si un dernier trade existe, obtenir le numéro de position actuel
        total_trades = last_trade.get('totaltrade', 0)
    else:
        # Aucun trade dans la collection, initialiser le numéro de position à 0
        total_trades = 0

    # Ajouter 1 pour le nouveau trade
    total_trades += 1

    # Insérer le numéro de position pour le nouveau trade dans la collection
    # Notez qu'ici, nous n'essayons pas de mettre à jour les trades précédents
    current_timestamp = datetime.now()
    new_trade = {'totaltrade': total_trades, 'timestamp': current_timestamp}  # Les détails du nouveau trade ici
    collection.insert_one(new_trade)

    return jsonify({'message': 'Numéro de position ajouté à chaque trade avec succès.'})

if __name__ == "__main__":
    app.run(debug=True)
