from flask import Flask, request, jsonify, Blueprint
from pymongo import MongoClient, DESCENDING

app = Flask(__name__)
client = MongoClient("mongodb+srv://pierre:ztxiGZypi6BGDMSY@atlascluster.sbpp5xm.mongodb.net/test?retryWrites=true&w=majority")
db = client["test"]

@Equity.route('/equity', methods=['GET'])
def calculate_equity(data):
    latest_entry = db.test2_close.find({}, sort=[("Equity", DESCENDING)], limit=1)

    # Vérifier si latest_entry est non vide
    if latest_entry.count() > 0:
        # Récupérer la première entrée (la dernière valeur) et extraire la clé "Equity"
        previous_entry = latest_entry[0].get("Equity", 2)
    else:
        previous_entry = 2  # Valeur par défaut si la collection est vide

    profit = data['profit']

    equity = profit + previous_entry

    return str(equity)

