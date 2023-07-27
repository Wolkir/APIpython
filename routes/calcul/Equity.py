from flask import Flask, request, jsonify, Blueprint
from pymongo import MongoClient, DESCENDING

app = Flask(__name__)
client = MongoClient("mongodb+srv://pierre:ztxiGZypi6BGDMSY@atlascluster.sbpp5xm.mongodb.net/test?retryWrites=true&w=majority")
db = client["test"]

Equity = Blueprint('Equity', __name__)

@Equity.route('/equity', methods=['GET'])
def calculate_equity(data):
    # Récupérer la dernière valeur de la clé "Equity" triée par ordre décroissant
    latest_entry = db.test2_close.find_one({}, sort=[("Equity", DESCENDING)])
    
    # Mettre à jour previous_equity avec la dernière valeur de "Equity" si elle existe, sinon garder la valeur par défaut de 2
    previous_equity = latest_entry.get("Equity", 2)
    
    profit = data['profit']
    equity = profit + previous_equity

    return equity
    

