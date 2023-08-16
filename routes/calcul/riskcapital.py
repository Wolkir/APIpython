from flask import Flask, Blueprint, jsonify
from pymongo import MongoClient

risk = Blueprint('risk', __name__)

# Connexion à la base de données MongoDB
client = MongoClient('mongodb+srv://pierre:ztxiGZypi6BGDMSY@atlascluster.sbpp5xm.mongodb.net/?retryWrites=true&w=majority')
db = client['test']


@risk.route('/risk', methods=['GET'])
def calculate_risk(data):
 
    point = data.get('point')
    tick= data.get('tick')
    SL = data.get('stopLoss')
    Entry = data.get('priceOpening')
    Volume = data.get('volume')

    capitalrisk = (Entry - SL)*Volume*tick*(1/point)
    return capitalrisk
