from flask import Blueprint, jsonify, request
from pymongo import MongoClient

# Connexion à la base de données MongoDB
client = MongoClient('mongodb+srv://pierre:ztxiGZypi6BGDMSY@atlascluster.sbpp5xm.mongodb.net/?retryWrites=true&w=majority')

tprbp = Blueprint('tprbp', __name__)
@tprbp.route('/tpr', methods=['GET'])
def calculate_tpr(data):
    # Your TPR calculation logic here based on the 'entry' data
    # For example:
    orderType = data.get('orderType')
    price_closure = data.get('priceClosure')
    take_profit = data.get('takeProfit')
    
    if orderType == "BUY" and price_closure >= take_profit and take_profit>0:
        entry['TPR'] = True
    elif orderType == "SELL" and price_closure <= take_profit and take_profit>0 :
        entry['TPR'] = True
    else:
        entry['TPR'] = False

    return entry
