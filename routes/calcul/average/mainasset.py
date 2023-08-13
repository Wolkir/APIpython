from flask import Flask, Blueprint, jsonify, request
from pymongo import MongoClient

mainasset = Blueprint('mainasset', __name__)

# Connexion à la base de données MongoDB
client = MongoClient('mongodb+srv://pierre:ztxiGZypi6BGDMSY@atlascluster.sbpp5xm.mongodb.net/?retryWrites=true&w=majority')
db = client['test']

@mainasset.route('/most_common_asset', methods=['GET'])
def most_common_asset(data):
    # Récupérer le username depuis les paramètres de la requête
    username = data.get('username')
    if not username:
        return jsonify({"error": "Username parameter is missing."}), 400

    # Définir les collections en fonction du username
    collection_name = f"{username}_close"
    collection = db[collection_name]
    
    collection_unit = f"{username}_unitaire"
    unitaire_collection = db[collection_unit]

    # Utiliser une opération d'agrégation pour compter la fréquence de chaque actif
    aggregation = [
        {
            "$group": {
                "_id": "$symbol",
                "count": {"$sum": 1}
            }
        },
        {
            "$sort": {"count": -1}
        },
        {
            "$limit": 1
        }
    ]
    
    most_common = list(collection.aggregate(aggregation))
    
    if most_common:
    # Convertir l'ObjectId en chaîne (si nécessaire)
       most_common[0]["_id"] = str(most_common[0]["_id"])
    
    # Préparez l'objet à insérer
     #  data_to_insert = {
     #      "mainasset": most_common[0]["_id"]       
    #}

    # Ajoutez l'objet à la collection unitaire
       unitaire_collection.update_one({}, {"$set": {"mainasset": most_common}}, upsert=True)

    # Renvoyez une réponse (cela dépend de ce que vous voulez renvoyer)
       return "Data added successfully"
