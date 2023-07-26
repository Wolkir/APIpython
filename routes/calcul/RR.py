from flask import Blueprint
from pymongo import MongoClient

# Connexion à la base de données MongoDB
client = MongoClient('mongodb+srv://pierre:ztxiGZypi6BGDMSY@atlascluster.sbpp5xm.mongodb.net/?retryWrites=true&w=majority')
db = client['test']

RR = Blueprint('RR', __name__)
@RR.route('/rr', methods=['GET'])

def calculate_rr(data):
  
    price_close = data['priceClosure']
    price_opening = data['priceOpening']
    stop_loss = data['stopLoss']
    rr = (price_close - price_opening) / (price_opening - stop_loss)

    return rr  # Renvoie la valeur de la clé "RR"

