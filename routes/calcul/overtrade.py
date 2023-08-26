from flask import Flask, Blueprint, jsonify, request
from pymongo import MongoClient

overtrade = Blueprint('overtrade', __name__)

# Connexion à la base de données MongoDB
client = MongoClient('mongodb+srv://pierre:ztxiGZypi6BGDMSY@atlascluster.sbpp5xm.mongodb.net/?retryWrites=true&w=majority')
db = client['test']

@overtrade.route('/overtrade', methods=['GET'])
def find_overtrade(data):
     
    tradecount = data.get('tradecount')
    
    if tradecount is None:
        return "Invalid Input", 400

    if tradecount > 5:
        overtrade = True
    else:
        overtrade = False

    return overtrade







