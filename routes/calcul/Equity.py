from flask import Flask, request, jsonify, Blueprint
from pymongo import MongoClient


app = Flask(__name__)
client = MongoClient("mongodb+srv://pierre:ztxiGZypi6BGDMSY@atlascluster.sbpp5xm.mongodb.net/test?retryWrites=true&w=majority")
db = client["test"]

Equity = Blueprint('Equity', __name__)

@Equity.route('/equity', methods=['POST'])
def calculate_equity():
    data = request.get_json()

    if 'profit' in data and isinstance(data['profit'], (int, float)):
        previous_equity = 2
        profit = data['profit']
        equity = previous_equity + profit
        return str(equity)  # Retourne la valeur de l'équité sous forme de chaîne de caractères
    else:
        return 'Invalid data. Expected JSON with "profit" field as a number.', 400
