from flask import Flask, Blueprint, jsonify, request
from pymongo import MongoClient

app = Flask(__name__)

# Connexion à la base de données MongoDB
client = MongoClient('mongodb+srv://pierre:ztxiGZypi6BGDMSY@atlascluster.sbpp5xm.mongodb.net/?retryWrites=true&w=majority')
db = client['test']

# Blueprint pour les routes profitfactorgroup
profitfactorgroup= Blueprint('profitfactorgroup', __name__)

@profitfactorgroup.route('/profitfactorgroup', methods=['GET'])

# Fonction pour calculer le profit factor
def calculate_profit_factor_custom(collection, filter_query):
    total_profit = 0
    total_loss = 0

    # Parcourir les documents de la collection
    for doc in collection.find(filter_query):
        profit = doc['profit']
        if profit > 0:
            total_profit += profit
        elif profit < 0:
            total_loss += profit

    # Calcul du profit factor
    profit_factor = total_profit / abs(total_loss)

    return total_profit, total_loss, profit_factor


def calculate_profit_factor_group():
    username = request.args.get('username')
    collection_name = f"{username}_close"
    collection_unitaire = f"{username}_unitaire"
    collection = db[collection_name]
    transaction_type = request.args.get('type')  # Paramètre pour spécifier le type de transaction (buy, sell ou all)

    if transaction_type == 'buy':
        filter_query = {"typeOfTransaction": "Buy"}
    elif transaction_type == 'sell':
        filter_query = {"typeOfTransaction": "Sell"}
    else:
        filter_query = {}

    total_profit, total_loss, profit_factor = calculate_profit_factor_custom(collection, filter_query)
    unitaire_collection = db[collection_unitaire]

    if transaction_type == 'buy':
        unitaire_collection.update_one({}, {'$set': {'profitfactor_long': profit_factor}}, upsert=True)
        unitaire_collection.update_one({}, {'$set': {'total_loss_long': total_loss}}, upsert=True)
        unitaire_collection.update_one({}, {'$set': {'total_gain_long': total_profit}}, upsert=True)
    elif transaction_type == 'sell':
        unitaire_collection.update_one({}, {'$set': {'profitfactor_short': profit_factor}}, upsert=True)
        unitaire_collection.update_one({}, {'$set': {'total_loss_short': total_loss}}, upsert=True)
        unitaire_collection.update_one({}, {'$set': {'total_gain_short': total_profit}}, upsert=True)
    else:
        unitaire_collection.update_one({}, {'$set': {'profitfactor_all': profit_factor}}, upsert=True)
        unitaire_collection.update_one({}, {'$set': {'total_loss_all': total_loss}}, upsert=True)
        unitaire_collection.update_one({}, {'$set': {'total_gain_all': total_profit}}, upsert=True)

   



