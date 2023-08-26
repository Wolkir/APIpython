from flask import Flask, Blueprint, jsonify, request
from pymongo import MongoClient
from datetime import datetime

tradecount = Blueprint('tradecount', __name__)

# Connexion à la base de données MongoDB
client = MongoClient('mongodb+srv://pierre:ztxiGZypi6BGDMSY@atlascluster.sbpp5xm.mongodb.net/?retryWrites=true&w=majority')
db = client['test']


@tradecount.route('/tradecount', methods=['GET'])
def calculate_tradecount(data):

    username = data.get('username')
    raw_date = data.get('dateAndTimeOpening')
    status = data.get('closurePosition')  # "open" ou "close"
   
    if not raw_date:
        return jsonify({"error": "Date not provided"}), 400

    try:
        date_of_trade = datetime.strptime(raw_date, '%Y-%m-%dT%H:%M:%S.%f%z').strftime('%Y-%m-%d')
    except ValueError as e:
        return jsonify({"error": str(e)}), 400

    collection_close = db[f"{username}_close"]
    collection_open = db[f"{username}_open"]

    multiple = False  # Initializing the multiple variable

    if status == "Open":
        count_close = collection_close.count_documents({"dateAndTimeOpening": {"$regex": f"^{date_of_trade}"}})
        count_open = collection_open.count_documents({"dateAndTimeOpening": {"$regex": f"^{date_of_trade}"}})
        
        # Check if another order is already open
        if count_open > 0:
            multiple = True
        
        new_trade_number = count_close + count_open + 1

    elif status == "Close":
        last_closed_trade = collection_close.find_one({"dateAndTimeOpening": {"$regex": f"^{date_of_trade}"}}, sort=[("tradecount", -1)])
        if last_closed_trade:
            new_trade_number = last_closed_trade["tradecount"] + 1
        else:
            new_trade_number = 1
    else:
        return jsonify({"error": f"Invalid status value: {status}"}), 400

    return new_trade_number


@tradecount.route('/checkmultiple', methods=['GET'])
def check_multiple_trades(data):

    username = data.get('username')
    raw_date = data.get('dateAndTimeOpening')
    status = data.get('closurePosition')

    if not raw_date:
        return jsonify({"error": "Date not provided"}), 400

    try:
        date_of_trade = datetime.strptime(raw_date, '%Y-%m-%dT%H:%M:%S.%f%z').strftime('%Y-%m-%d')
    except ValueError as e:
        return jsonify({"error": str(e)}), 400

    collection_name = f"{username}_temporaire"
    collection = db[collection_name]
    collection_open = db[f"{username}_open"]

    if status == "Open":
        count_open = collection_open.count_documents({"dateAndTimeOpening": {"$regex": f"^{date_of_trade}"}})

        # Check if another order is already open
        multiple = count_open > 0

        # Stocker la valeur de 'multiple' dans la collection 'username_unitaire'
        collection.insert_one({
            "username": username,
            "dateAndTimeOpening": raw_date,
            "multiple": multiple
        })

    elif status == "Close":
        # Récupérer la valeur de 'multiple' de la collection 'username_unitaire'
        order_data = collection.find_one({"username": username, "dateAndTimeOpening": {"$regex": f"^{date_of_trade}"}})
        multiple = order_data["multiple"] if order_data else False

        # Supprimer l'entrée correspondante dans la collection 'username_unitaire'
        collection.delete_one({"username": username, "dateAndTimeOpening": {"$regex": f"^{date_of_trade}"}})

    else:
        return jsonify({"error": f"Invalid status value: {status}"}), 400

    return multiple
