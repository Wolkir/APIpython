from flask import Flask, Blueprint, jsonify
from pymongo import MongoClient

minloss = Blueprint('minloss', __name__)

# Connexion à la base de données MongoDB
client = MongoClient('mongodb+srv://pierre:ztxiGZypi6BGDMSY@atlascluster.sbpp5xm.mongodb.net/?retryWrites=true&w=majority')
db = client['test']
collection = db['things']

@minloss.route('/minloss', methods=['GET'])
def find_min_loss():
    # Recherche de la ligne avec le profit < 0 le plus petit
    min_loss = collection.find_one({"profit": {"$lt": 0}}, sort=[("profit", 1)])

    if min_loss:
        loss_value = min_loss['profit']
        unitaire_collection = db['unitaire']
        unitaire_collection.insert_one({"maxloss": loss_value})
        return jsonify({"min_loss": loss_value})
    else:
        return jsonify({"message": "Aucune ligne avec profit < 0 trouvée"})
