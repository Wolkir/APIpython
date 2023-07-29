from flask import Flask, jsonify, request
from pymongo import MongoClient

app = Flask(__name__)
profitfactorgrpup = Blueprint('profitfactorgroup', __name__)
# Connexion à la base de données MongoDB
client = MongoClient('mongodb+srv://pierre:ztxiGZypi6BGDMSY@atlascluster.sbpp5xm.mongodb.net/?retryWrites=true&w=majority')
db = client['test']

@app.route('/profitfactorgroup', methods=['GET'])
def calculate_profit_factor_group():
    username = request.args.get('username')
    transaction_type = request.args.get('type', None)

    collection_name = f"{username}_close"
    collection_unitaire = f"{username}_unitaire"
    collection = db[collection_name]

    # Calcul du profit total et de la perte totale pour les transactions du type spécifié
    total_profit = 0
    total_loss = 0

    # Parcourir les documents de la collection
    filter_query = {} if transaction_type is None else {"typeOfTransaction": transaction_type}

    for doc in collection.find(filter_query):
        profit = doc['profit']
        if profit > 0:
            total_profit += profit
        elif profit < 0:
            total_loss += profit

    # Calcul du profit factor
    profit_factor = total_profit / abs(total_loss)

    # Insérer le profit factor dans la collection "unitaire"
    unitaire_collection = db[collection_unitaire]
    if transaction_type is None:
        unitaire_collection.update_one({}, {'$set': {'profitfactor': profit_factor}}, upsert=True)
        unitaire_collection.update_one({}, {'$set': {'total loss': total_loss}}, upsert=True)
        unitaire_collection.update_one({}, {'$set': {'total gain': total_profit}}, upsert=True)
    elif transaction_type == "Buy":
        unitaire_collection.update_one({}, {'$set': {'profitfactorlong': profit_factor}}, upsert=True)
        unitaire_collection.update_one({}, {'$set': {'total loss long': total_loss}}, upsert=True)
        unitaire_collection.update_one({}, {'$set': {'total gain long': total_profit}}, upsert=True)
