from flask import Flask, Blueprint, jsonify
from pymongo import MongoClient

maxprofit = Blueprint('maxprofit', __name__)

# Connexion à la base de données MongoDB
client = MongoClient('mongodb+srv://pierre:ztxiGZypi6BGDMSY@atlascluster.sbpp5xm.mongodb.net/?retryWrites=true&w=majority')
db = client['test']
collection = db['things']

@maxprofit.route('/maxprofit', methods=['GET'])
def find_max_profit():
    # Recherche de la ligne avec le profit > 0 le plus grand
    max_profit = collection.find_one({"profit": {"$gt": 0}}, sort=[("profit", -1)])

    if max_profit:
        profit_value = max_profit['profit']
        
        unitaire_collection = db['unitaire']
        unitaire_collection.insert_one({"maxprofit": profit_value})
        return jsonify({"max_profit": profit_value})
        
    else:
        return jsonify({"message": "Aucune ligne avec profit > 0 trouvée"})
