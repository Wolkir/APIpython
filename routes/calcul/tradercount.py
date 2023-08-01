from flask import Flask, Blueprint, jsonify, request
from pymongo import MongoClient
from datetime import datetime

tradercount = Blueprint('tradercount', __name__)

client = MongoClient('mongodb+srv://pierre:ztxiGZypi6BGDMSY@atlascluster.sbpp5xm.mongodb.net/?retryWrites=true&w=majority')
db = client['test']
# Variable globale pour stocker le tradercount de la journée en cours
daily_trade_counts = {}

@tradercount.route('/tradercount', methods=['GET'])
def calculate_tradercount(data):
    try:
        username = data.get('username')

        collection_close = f"{username}_close"
        # Collection pour stocker les trades ouverts
        collection_open = f"{username}_open"

        # Recherche de la dernière position fermée pour la date actuelle
        current_date = datetime.now().strftime('%Y-%m-%dT%H:%M:%S.%f%z')
        print("Current Date:", current_date)

        last_trade = db[collection_close].find_one({'date': current_date}, sort=[('tradecount', -1)])
        print("Last Trade:", last_trade)

        # Si aucun trade n'a été fermé aujourd'hui, alors le tradecount sera 1 pour la position ouverte
        if not last_trade:
            tradecount = 1
        else:
            tradecount = last_trade['tradecount'] + 1

        # Mettre à jour le tradercount de la journée en cours dans la variable globale
        daily_trade_counts[current_date] = tradecount

        # Renvoyer la valeur du tradecount
        print("TradeCount:", tradecount)
        return str(tradecount)  # Renvoyer le tradecount en tant que chaîne de caractères

    except Exception as e:
        print("Error:", e)
        return jsonify({'error': str(e)}), 500
