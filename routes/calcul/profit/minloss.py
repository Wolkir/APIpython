from flask import Flask, Blueprint, jsonify
from pymongo import MongoClient

minloss = Blueprint('minloss', __name__)

# Connexion à la base de données MongoDB
client = MongoClient('mongodb+srv://pierre:ztxiGZypi6BGDMSY@atlascluster.sbpp5xm.mongodb.net/?retryWrites=true&w=majority')
db = client['test']


@minloss.route('/minloss', methods=['GET'])
def find_min_loss(data):
    username = data.get('username')
    collection_name = f"{username}_close"
    collection_unitaire = f"{username}_unitaire"
    collection = db[collection_name]
    # Recherche de la ligne avec le profit < 0 le plus petit
    min_loss = collection.find_one({"profit": {"$lt": 0}}, sort=[("profit", 1)])

    if min_loss:
        loss_value = min_loss['profit']
        unitaire_collection = db[collection_unitaire]
        unitaire_collection.update_one({}, {'$set': {'Max loss': (loss_value)}}, upsert=True)
 
