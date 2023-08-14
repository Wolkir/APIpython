
from flask import Flask, Blueprint, jsonify, request
from pymongo import MongoClient

profitw = Blueprint('profitw', __name__)

# Connexion à la base de données MongoDB
client = MongoClient('mongodb+srv://pierre:ztxiGZypi6BGDMSY@atlascluster.sbpp5xm.mongodb.net/?retryWrites=true&w=majority')
db = client['test']

@profitw.route('/profitw', methods=['GET'])
def calculate_profitw(data):
    
    # Récupération des données depuis la requête
    username = data.get('username')
    collection_name = f"{username}_close"
    collection = db[collection_name]

    # Création du pipeline d'agrégation pour sommer les profits par semaine
    pipeline = [
        {
            "$group": {
                "_id": {
                    "year": {"$year": "$date"},  # Utilisation de la clé "date" pour déterminer l'année
                    "week": {"$week": "$date"}   # Utilisation de la clé "date" pour déterminer le numéro de la semaine
                },
                "totalProfit": {"$sum": "$profit"}  # Utilisation de la clé "profit" pour représenter le profit journalier
            }
        },
        {
            "$project": {
                "weeknumber": "$_id.week",
                "profitw": "$totalProfit",
                "_id": 0
            }
        }
    ]

    # Exécution du pipeline d'agrégation
    collection.aggregate(pipeline)

# Récupérez les résultats de la nouvelle collection pour les renvoyer en tant que réponse
    weekly_profit_collection = db[f"{username}_weekly_profit"]
    results = list(weekly_profit_collection.find({}))

    return jsonify(results)
