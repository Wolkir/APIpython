from flask import Flask, Blueprint, jsonify
from pymongo import MongoClient
from routes.calcul.RR import calculate_rr

BE = Blueprint('BE', __name__)

# Connexion à la base de données MongoDB
client = MongoClient('mongodb+srv://pierre:ztxiGZypi6BGDMSY@atlascluster.sbpp5xm.mongodb.net/?retryWrites=true&w=majority')
db = client['test']

def find_BE(data):
    price_close = data['priceClosure']
    price_opening = data['priceOpening']
    stop_loss = data['stopLoss']
    rrcalculation = (price_close - price_opening) / (price_opening - stop_loss)
    rrcalculation = round(rrcalculation, 2)

    #resultBE = {}  # Initialize the 'resultBE' dictionary

    if data['closurePosition'] == "Close" and -0.5 < rrcalculation < 0.5:
        resultBE = True
    else:
        resultBE= False

    return resultBE  # Renvoie la valeur de BE
