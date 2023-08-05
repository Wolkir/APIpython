from flask import Flask, Blueprint, jsonify, request
from pymongo import MongoClient
from datetime import datetime

tradercount = Blueprint('tradercount', __name__)

client = MongoClient('mongodb+srv://pierre:ztxiGZypi6BGDMSY@atlascluster.sbpp5xm.mongodb.net/?retryWrites=true&w=majority')
db = client['test']
# Variable globale pour stocker le tradercount de la journée en cours
daily_trade_counts = {}

@tradercount.route('/tradercount', methods=['GET'])
@tradercount.route('/tradercount', methods=['GET'])
def calculate_tradercount(data):
    try:
        username = data.get('username')

        collection_close = f"{username}_close"

        # Rechercher le dernier trade (le trade avec le tradecount le plus élevé)
        last_trade = db[collection_close].find_one(sort=[('tradecount', -1)])

        # Si aucun trade n'a été fait jusqu'à présent, alors le tradecount sera 1 pour le nouveau trade
        if not last_trade:
            tradecount = 1
        else:
            # Sinon, le tradecount du nouveau trade sera le tradecount du dernier trade + 1
            tradecount = last_trade['tradecount'] + 1

        print("TradeCount:", tradecount)
        return str(tradecount)

    except Exception as e:
        print("Error:", e)
        return jsonify({'error': str(e)}), 500
