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
    try:
        username = data.get('username')

        collection_close = f"{username}_close"

        # Rechercher le dernier trade (le trade avec le totaltrade le plus élevé)
        last_trade = db[collection_close].find_one(sort=[('totaltrade', -1)])

        # Si aucun trade n'a été fait jusqu'à présent, alors le totaltrade sera 1 pour le nouveau trade
        if not last_trade:
            totaltrade = 1
        else:
            # Sinon, le totaltrade du nouveau trade sera le totaltrade du dernier trade + 1
            totaltrade = last_trade['totaltrade'] + 1

        print("totaltrade:", totaltrade)
        return str(totaltrade)

    except Exception as e:
        print("Error:", e)
        return jsonify({'error': str(e)}), 500
