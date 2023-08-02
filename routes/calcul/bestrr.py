from flask import Flask, Blueprint, jsonify
from pymongo import MongoClient
from datetime import timedelta

app = Flask(__name__)
bestrr = Blueprint('bestrr', __name__)

# Connexion à la base de données MongoDB
client = MongoClient('mongodb+srv://pierre:ztxiGZypi6BGDMSY@atlascluster.sbpp5xm.mongodb.net/?retryWrites=true&w=majority')
db = client['test']

@bestrr.route('/best', methods=['GET'])
def calculate_best_rr():
    collection = db["test2_close"]

    best_rr = 0
    best_day = ""
    best_symbol = ""
    best_order_type = ""

    rr_by_combination = {}  # Dictionnaire pour stocker la somme des RR pour chaque combinaison (Day, symbol, orderType)
    rr_count_combination = {}  # Dictionnaire pour stocker le nombre de RR pour chaque combinaison

    # Parcourir les documents de la collection et calculer la somme des RR pour chaque combinaison
    for doc in collection.find():
        rr_value = doc.get('RR', 0)
        day = doc.get('Day')
        symbol = doc.get('symbol')
        order_type = doc.get('orderType')
        combination = (day, symbol, order_type)

        if rr_value is not None:
            rr_by_combination[combination] = rr_by_combination.get(combination, 0) + rr_value
            rr_count_combination[combination] = rr_count_combination.get(combination, 0) + 1

    for combination, rr_total in rr_by_combination.items():
        rr_count = rr_count_combination.get(combination, 0)
        average_rr = rr_total / rr_count if rr_count > 0 else 0

        if average_rr > best_rr:
            best_rr = average_rr
            best_day, best_symbol, best_order_type = combination

    response = {
        'best_day': best_day,
        'best_symbol': best_symbol,
        'best_order_type': best_order_type,
        'best_rr': best_rr
    }

    return jsonify(response)
