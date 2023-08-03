from flask import Flask, Blueprint, jsonify
from pymongo import MongoClient
from datetime import datetime, timedelta

app = Flask(__name__)
daytrade = Blueprint('daytrade', __name__)

# Connexion à la base de données MongoDB
client = MongoClient('mongodb+srv://pierre:ztxiGZypi6BGDMSY@atlascluster.sbpp5xm.mongodb.net/?retryWrites=true&w=majority')
db = client['test']

@daytrade.route('/daytrade', methods=['GET'])
def calculate_daytrade(data):

    username = data.get('username')
    collection_name_open = f"{username}_open"

    collection_open = db[collection_name_open]

    # Obtenir la date actuelle
    current_date = datetime.now()

    # Rechercher les trades ouverts dans la journée
    daytrades_open = collection_open.find({"timestamp": {"$gte": datetime(current_date.year, current_date.month, current_date.day)}})

    # Trouver le numéro de "daytrade" maximal parmi les trades ouverts dans la journée
    max_daytrade = 0
    for trade in daytrades_open:
        daytrade_value = trade.get('daytrade', 0)
        if daytrade_value > max_daytrade:
            max_daytrade = daytrade_value

    # Calculer le numéro de "daytrade" pour le nouveau trade ouvert
    daytrade_value = max_daytrade + 1

    return jsonify({'message': 'Numéro de daytrade calculé.', 'daytrade': daytrade_value})

if __name__ == "__main__":
    app.run(debug=True)
