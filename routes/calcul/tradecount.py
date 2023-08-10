from flask import Flask, Blueprint, jsonify, request
from pymongo import MongoClient
from datetime import datetime

tradecount = Blueprint('tradecount', __name__)

# Connexion à la base de données MongoDB
client = MongoClient('mongodb+srv://pierre:ztxiGZypi6BGDMSY@atlascluster.sbpp5xm.mongodb.net/?retryWrites=true&w=majority')
db = client['test']

@tradecount.route('/tradecount', methods=['POST'])  # J'ai changé GET en POST car il semble que vous souhaitez soumettre des données
def calculate_tradecount(data):
    
    data = request.json
    username = data.get('username')
    date_of_trade = data.get('date') or datetime.now().strftime('%Y-%m-%d')
    
    collection_close = db[f"{username}_close"]
    collection_open = db[f"{username}_open"]

    # Comptez les trades fermés et ouverts pour la date donnée
    count_close = collection_close.count_documents({"date": date_of_trade})
    count_open = collection_open.count_documents({"date": date_of_trade})

    # Calculer le numéro de trade pour le nouveau trade
    new_trade_number = count_close + count_open + 1

    # À ce stade, vous pouvez soit ajouter ce nouveau trade à la collection appropriée, soit renvoyer ce numéro.

    return jsonify({"new_trade_number": new_trade_number})

if __name__ == "__main__":
    app = Flask(__name__)
    app.register_blueprint(tradecount)
    app.run(debug=True)
