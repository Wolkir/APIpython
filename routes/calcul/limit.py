from flask import Flask, Blueprint, jsonify
from pymongo import MongoClient


limit = Blueprint('limit', __name__)

# Connexion à la base de données MongoDB
client = MongoClient('mongodb+srv://pierre:ztxiGZypi6BGDMSY@atlascluster.sbpp5xm.mongodb.net/?retryWrites=true&w=majority')
db = client['test']

def find_limit(data):
    
    orderType = data['orderType']
    
    if orderType != "BUY" and orderType != "SELL":
        condi = True
    else:
        condi = False
    return condi  # Renvoie la valeur de BE
