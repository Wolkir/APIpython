from flask import Flask, request, jsonify, Blueprint
from pymongo import MongoClient, DESCENDING

app = Flask(__name__)
client = MongoClient("mongodb+srv://pierre:ztxiGZypi6BGDMSY@atlascluster.sbpp5xm.mongodb.net/test?retryWrites=true&w=majority")
db = client["test"]

Equity = Blueprint('Equity', __name__)

@Equity.route('/equity', methods=['GET'])
def calculate_equity(data):
    latest_entry = db.test2_close.find_one({}, sort=[("Equity", DESCENDING)])

    # Vérifier si latest_entry existe et si "Equity" est une valeur numérique (int ou float)
    if latest_entry and isinstance(latest_entry["Equity"], (float, int)):
        previous_entry = float(latest_entry["Equity"])
    else:
        previous_entry = 2.0  # Valeur par défaut si "Equity" n'est pas un nombre ou latest_entry est None

    profit = data['profit']

    equity = profit + previous_entry

    return str(equity)




