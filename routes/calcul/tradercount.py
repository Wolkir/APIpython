from flask import Flask, Blueprint, jsonify, request
from pymongo import MongoClient

tradecount = Blueprint('tradecount', __name__)

# Variable globale pour stocker le tradercount de la journée en cours
tradercount_today = 0

@tradecount.route('/tradecount/close', methods=['GET'])
def tradecount(data):
    global tradercount_today

    
    username = data.get('username')

    # Se connecter à la base de données
    client = MongoClient('mongodb+srv://pierre:ztxiGZypi6BGDMSY@atlascluster.sbpp5xm.mongodb.net/?retryWrites=true&w=majority')
    db = client['test']

    # Identifier la collection appropriée en fonction du type de trade
    if data.get("trade_type") == "Close":
        collection_name = f"{username}_close"
    else:
        collection_name = f"{username}_open"

        # Vérifier si le dernier trade "Close" était le même jour que l'ordre "Open" actuel
        last_close_trade = db[f"{username}_close"].find_one(sort=[("dateAndTimeClosing", -1)])
        if last_close_trade is not None:
            last_close_date = last_close_trade.get("dateAndTimeClosing")
            current_open_date = data.get("dateAndTimeOpening")
            if last_close_date.date() == current_open_date.date():
                tradercount_today = last_close_trade.get("tradercount", 0)

    # Incrémenter le tradercount pour le nouvel ordre
    tradercount_today += 1

    # Ajouter le nouvel ordre avec le tradercount mis à jour
    collection = db[collection_name]
    new_trade = {
        "dateAndTimeOpening": data.get("dateAndTimeOpening"),
        "dateAndTimeClosing": data.get("dateAndTimeClosing"),
        "tradercount": tradercount_today
    }
    collection.insert_one(new_trade)

