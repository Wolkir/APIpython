from flask import Flask, Blueprint, jsonify
from pymongo import MongoClient

risk = Blueprint('risk', __name__)

# Connexion à la base de données MongoDB
client = MongoClient('mongodb+srv://pierre:ztxiGZypi6BGDMSY@atlascluster.sbpp5xm.mongodb.net/?retryWrites=true&w=majority')
db = client['test']


@risk.route('/risk', methods=['GET'])
def calculate_risk(data):
 
    point = float(data.get('point', 1))
    tick = float(data.get('tick', 1))
    SL = float(data.get('stopLoss', 1))
    Entry = float(data.get('priceOpening', 1))
    Volume = float(data.get('volume', 1))

    capitalrisk = (Entry - SL) * Volume * tick * (1/point)
    return capitalrisk
