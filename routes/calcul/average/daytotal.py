from flask import Flask, Blueprint, jsonify
from pymongo import MongoClient
from datetime import datetime, timedelta
from routes.calcul.totaltrade import calculate_totaltrade

daytotal = Blueprint('daytotal', __name__)

# Connexion à la base de données MongoDB
client = MongoClient('mongodb+srv://pierre:ztxiGZypi6BGDMSY@atlascluster.sbpp5xm.mongodb.net/?retryWrites=true&w=majority')
db = client['test']


@daytotal.route('/daytotal', methods=['POST'])  # POST pour la sécurité des données de l'utilisateur
def calculate_daycount(data):
   
    username = data.get('username')
    
    if not username:
        return jsonify({"error": "Username is required!"}), 400

    collection_name = f"{username}_close"
    collection = db[collection_name]
    collection_unit = f"{username}_unitaire"
    unitaire_collection = db[collection_unit]
    

    # Supposition qu'il y a un champ 'date' dans chaque document contenant la date
    distinct_dates = collection.aggregate([
    {
        "$addFields": {
            "dateParts": {
                "$split": ["$dateAndTimeOpening", "."]
            }
        }
    },
    {
        "$addFields": {
            "convertedDate": {
                "$dateFromString": {
                    "dateString": {
                        "$arrayElemAt": ["$dateParts", 0]
                    },
                    "format": "%Y-%m-%dT%H:%M:%S"
                }
            }
        }
    },
    {
        "$group": {
            "_id": {
                "year": {"$year": "$convertedDate"},
                "month": {"$month": "$convertedDate"},
                "day": {"$dayOfMonth": "$convertedDate"},
            }
        }
    },
    {
        "$count": "distinctDateCount"
    }
])
    result = list(distinct_dates)
    if result:
        distinct_count = result[0]['distinctDateCount']
        unitaire_collection.update_one({}, {"$set": {"daytotal": distinct_count}}, upsert=True)
        return jsonify({"distinctDateCount": distinct_count})
   
    return jsonify({"error": "No distinct dates found"}), 400


@app.route('/averagedaytrade', methods=['POST'])
def calculate_averagedaytrade():
    data = request.json
    username = data.get('username')

    if not username:
        return jsonify({"error": "Username is required!"}), 400

    # Récupérer le nombre total de trades
    collection_name = f"{username}_close"
    collection = db[collection_name]
    total_trades = collection.count_documents({})

    # Récupérer le nombre total de jours
    distinct_dates = collection.aggregate([
        {"$addFields": {"dateParts": {"$split": ["$dateAndTimeOpening", "."]}}},
        {"$addFields": {"convertedDate": {"$dateFromString": {"dateString": {"$arrayElemAt": ["$dateParts", 0]}, "format": "%Y-%m-%dT%H:%M:%S"}}}},
        {"$group": {"_id": {"year": {"$year": "$convertedDate"}, "month": {"$month": "$convertedDate"}, "day": {"$dayOfMonth": "$convertedDate"}}}},
        {"$count": "distinctDateCount"}
    ])
    result = list(distinct_dates)
    if result:
        distinct_count = result[0]['distinctDateCount']
    else:
        return jsonify({"error": "No distinct dates found"}), 400

    # Calculer la moyenne
    average_trades_per_day = total_trades / distinct_count

    # Mettre à jour la collection MongoDB
    collection_unit = f"{username}_unitaire"
    unitaire_collection = db[collection_unit]
    unitaire_collection.update_one({}, {"$set": {"averagedaytrade": average_trades_per_day}}, upsert=True)

    return jsonify({"averageTradesPerDay": average_trades_per_day})

