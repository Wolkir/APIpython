from flask import Flask, request, jsonify, Blueprint
from pymongo import MongoClient, DESCENDING

app = Flask(__name__)
client = MongoClient("mongodb+srv://pierre:ztxiGZypi6BGDMSY@atlascluster.sbpp5xm.mongodb.net/test?retryWrites=true&w=majority")
db = client["test"]

Equity = Blueprint('Equity', __name__)

@Equity.route('/equity', methods=['GET'])
def calculate_equity():
    data = request.get_json()  # Assuming the data is passed as a JSON object in the request body

    # Récupérer la dernière valeur de la clé "Equity" triée par ordre décroissant
    latest_entry = db.test2_close.find_one({}, sort=[("Equity", DESCENDING)])
    
    # Mettre à jour previous_equity avec la dernière valeur de "Equity" si elle existe, sinon garder la valeur par défaut de 2
    previous_equity = latest_entry.get("Equity", 2)
    
    # Récupérer la valeur du profit à partir des données (assurez-vous que la clé "profit" existe dans les données)
    profit = data.get('profit', 0)
    
    # Vérifier si le profit est un nombre (float ou int)
    if not isinstance(profit, (float, int)):
        return jsonify({"error": "Profit must be a numeric value."}), 400
    
    equity = profit + previous_equity
    
       
    return equity

