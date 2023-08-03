from flask import Flask, Blueprint, jsonify
from pymongo import MongoClient
from datetime import datetime, timedelta

app = Flask(__name__)
averagetrade = Blueprint('averagetrade', __name__)

# Connexion à la base de données MongoDB
client = MongoClient('mongodb+srv://pierre:ztxiGZypi6BGDMSY@atlascluster.sbpp5xm.mongodb.net/?retryWrites=true&w=majority')
db = client['test']

@averagetrade.route('/averagetrade', methods=['GET'])
def calculate_averagetrade(data):

    username = data.get('username')
    collection_name = f"{username}_close"
    collection_unitaire = f"{username}_unitaire"
    collection = db[collection_name]

    # Calculer le nombre total de trades dans la collection
    total_trades = collection.count_documents({})

    if total_trades == 0:
        return jsonify({'message': 'Aucun trade dans la collection.', 'average_daily_trades': 0})

    # Obtenir le premier trade de la collection triée par ordre chronologique
    first_trade = collection.find_one(sort=[('timestamp', 1)])
    date_and_time_opening = datetime.strptime(first_trade['timestamp'], "%Y-%m-%dT%H:%M:%S.%f%z")

    # Obtenir le dernier trade de la collection triée par ordre chronologique
    last_trade = collection.find_one(sort=[('timestamp', -1)])
    date_and_time_closing = datetime.strptime(last_trade['timestamp'], "%Y-%m-%dT%H:%M:%S.%f%z")

    # Calculer le nombre de jours entre la date de début et la date de fin
    delta_days = (date_and_time_closing - date_and_time_opening).days

    # Calculer la moyenne journalière du nombre de trades
    if delta_days > 0:
        average_daily_trades = total_trades / delta_days
    else:
        average_daily_trades = total_trades

    return jsonify({'message': 'Moyenne journalière du nombre de trades calculée.', 'average_daily_trades': average_daily_trades})

if __name__ == "__main__":
    app.run(debug=True)
