from flask import Flask, Blueprint, jsonify
from pymongo import MongoClient

risk = Blueprint('risk', __name__)

# Connexion à la base de données MongoDB
client = MongoClient('mongodb+srv://pierre:ztxiGZypi6BGDMSY@atlascluster.sbpp5xm.mongodb.net/?retryWrites=true&w=majority')
db = client['test']


@risk.route('/risk', methods=['GET'])
def calculate_risk(data):
 
    point = float(request.args.get('point', 1))
    tick = float(request.args.get('tick', 1))
    SL = float(request.args.get('stopLoss', 1))
    Entry = float(request.args.get('priceOpening', 1))
    Volume = float(request.args.get('volume', 1))

    capitalrisk = (Entry - SL) * Volume * tick * (1/point)
    return capitalrisk
