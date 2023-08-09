from flask import Blueprint, jsonify, request
from pymongo import MongoClient

# Connexion à la base de données MongoDB
client = MongoClient('mongodb+srv://pierre:ztxiGZypi6BGDMSY@atlascluster.sbpp5xm.mongodb.net/?retryWrites=true&w=majority')

slrbp = Blueprint('slrbp', __name__)
@slrbp.route('/slr', methods=['GET'])
def calculate_slr(data):
    
    orderType = data.get('orderType')
    price_closure = data.get('priceClosure')
    stop_loss = data.get('stopLoss')
    profit = data.get('profit')

    if orderType == "BUY" and price_closure <= stop_loss and profit < 0:
        data['SLR'] = True
    elif orderType == "SELL" and price_closure >= stop_loss and profit < 0:
        data['SLR'] = True
    elif orderType == "BUY" and price_closure >= stop_loss and profit > 0:
        data['SLR'] = 'credit'  # Changed 'Credit' to 'credit'
    elif orderType == "SELL" and price_closure <= stop_loss and profit > 0:
        data['SLR'] = 'credit'  # Changed 'Credit' to 'credit'
    else:
        data['SLR'] = False

    return data
