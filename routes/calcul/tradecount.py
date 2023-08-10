from flask import Flask, Blueprint, jsonify, request
from pymongo import MongoClient
from datetime import datetime

tradecount = Blueprint('tradecount', __name__)

# Connexion à la base de données MongoDB
client = MongoClient('mongodb+srv://pierre:ztxiGZypi6BGDMSY@atlascluster.sbpp5xm.mongodb.net/?retryWrites=true&w=majority')
db = client['test']


@tradecount.route('/tradecount', methods=['GET'])
def calculate_tradecount():
    data = request.json
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

    if status == "Open":
        count_close = collection_close.count_documents({"dateAndTimeOpening": {"$regex": f"^{date_of_trade}"}})
        count_open = collection_open.count_documents({"dateAndTimeOpening": {"$regex": f"^{date_of_trade}"}})
        new_trade_number = count_close + count_open + 1

    elif status == "Close":
        last_closed_trade = collection_close.find_one({"dateAndTimeOpening": {"$regex": f"^{date_of_trade}"}}, sort=[("trade_number", -1)])
        if last_closed_trade:
            new_trade_number = last_closed_trade["trade_number"] + 1
        else:
            new_trade_number = 1
    else:
        return jsonify({"error": f"Invalid status value: {status}"}), 400

    return new_trade_number
