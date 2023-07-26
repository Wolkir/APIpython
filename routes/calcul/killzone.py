from flask import Blueprint, jsonify, request
from pymongo import MongoClient

# Connexion à la base de données MongoDB
client = MongoClient('mongodb+srv://pierre:ztxiGZypi6BGDMSY@atlascluster.sbpp5xm.mongodb.net/?retryWrites=true&w=majority')

tpr = Blueprint('tpr', __name__)

def calculate_tpr(entry):
    # Your TPR calculation logic here based on the 'entry' data
    # For example:
    type_of_transaction = entry.get('typeOfTransaction')
    price_closure = entry.get('priceClosure')
    take_profit = entry.get('takeProfit')
    
    if type_of_transaction == "Buy" and price_closure >= take_profit:
        entry['TPR'] = True
    elif type_of_transaction == "Sell" and price_closure <= take_profit:
        entry['TPR'] = True
    else:
        entry['TPR'] = False

    return entry
