from flask import Flask, request, jsonify, Blueprint
from pymongo import MongoClient, DESCENDING

app = Flask(__name__)
client = MongoClient("mongodb+srv://pierre:ztxiGZypi6BGDMSY@atlascluster.sbpp5xm.mongodb.net/test?retryWrites=true&w=majority")
db = client["test"]
Equity = Blueprint('Equity', __name__)

@Equity.route('/equity', methods=['GET'])
def calculate_equity(data):
    latest_entry_cursor = db.things_close.find({}, sort=[("_id", DESCENDING)], limit=1)

    # Vérifier si latest_entry_cursor contient des documents
    if latest_entry_cursor.count() > 0:
        latest_entry = latest_entry_cursor[0]
        # Vérifier si "Equity" existe dans latest_entry et est une valeur numérique (int ou float)
        if "Equity" in latest_entry and isinstance(latest_entry["Equity"], (float, int)):
            previous_entry = float(latest_entry["Equity"])
        else:
            previous_entry = 2.0  # Valeur par défaut si "Equity" n'est pas un nombre
    else:
        previous_entry = 2.0  # Valeur par défaut si la collection est vide

    profit = data['profit']

    equity = profit + previous_entry

    return equity
