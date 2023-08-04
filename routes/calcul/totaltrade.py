from flask import Flask, Blueprint, jsonify, request
from pymongo import MongoClient
from datetime import timedelta

app = Flask(__name__)
totaltrade = Blueprint('totaltrade', __name__)

# Connexion à la base de données MongoDB
client = MongoClient('mongodb+srv://pierre:ztxiGZypi6BGDMSY@atlascluster.sbpp5xm.mongodb.net/?retryWrites=true&w=majority')
db = client['test']

@totaltrade.route('/totaltrade', methods=['GET'])
def calculate_totaltrade():

    data = request.get_json()
    username = data.get('username')
    collection_name = f"{username}_close"
    collection = db[collection_name]

    # Obtenir le dernier trade de la collection triée par ordre chronologique
    last_trade = collection.find_one(sort=[('timestamp', -1)])

    # Assigner le numéro du trade en fonction de la présence du dernier trade
    if last_trade is None:
        total_trades = 1
    else:
        total_trades = last_trade.get('totaltrade', 0) + 1

    # Return the total trades
    return jsonify({'total_trades': total_trades})

if __name__ == "__main__":
    app.run(debug=True)
