from flask import Flask, Blueprint, jsonify
from pymongo import MongoClient

winrategroup = Blueprint('winrategroup', __name__)

# Connexion à la base de données MongoDB
client = MongoClient('mongodb+srv://pierre:ztxiGZypi6BGDMSY@atlascluster.sbpp5xm.mongodb.net/?retryWrites=true&w=majority')
db = client['test']


@winrategroup.route('/winrategroup', methods=['GET'])
def calculate_winrate_group(data):
    

    username = data.get('username')
    identifier = data.get('identifier')
    collection_name = f"{username}_close"
    collection_unitaire1 = f"{username}_unitaire"
    collection_unitaire = db[collection_unitaire1]
    collection = db[collection_name]

    # Récupérer tous les documents
    documents = list(collection.find())

    positive_profits_count = 0
    negative_profits_count = 0

    positive_identifiers = set()
    negative_identifiers = set()

    # Compter le nombre de documents avec profit > 0 et les identifiants uniques
    # pour le calcul du winrate standard et du winrate real
    for doc in documents:
        profit = doc['profit']
        identifier = doc['identifier']

        if profit > 0 and identifier not in positive_identifiers:
            positive_profits_count += 1
            positive_identifiers.add(identifier)
        elif profit < 0 and identifier not in negative_identifiers:
            negative_profits_count += 1
            negative_identifiers.add(identifier)

    # Calcul du winrate standard
    winratestd = positive_profits_count / (positive_profits_count + negative_profits_count) * 100

    # Compter le nombre de documents avec profit > 0 pour le calcul du winrate real
    positive_profits_count_real = collection.count_documents({"profit": {"$gt": 0}})

    # Compter le nombre de documents avec profit < 0 pour le calcul du winrate real
    negative_profits_count_real = collection.count_documents({"profit": {"$lt": 0}})

    # Calcul du winrate real
    winrate_value_real = positive_profits_count_real / (positive_profits_count_real + negative_profits_count_real) * 100

    # Insérer les deux winrates dans la collection "unitaire"
    collection_unitaire.update_one({}, {'$set': {'winratestdl2': winratestd, 'winratereal2': winrate_value_real}}, upsert=True)

    # Calculer RRT
    winrate = collection_unitaire.find_one({}, {"winratereal2": 1})["winratereal2"]
    risk_reward = collection_unitaire.find_one({}, {"RRaverage2": 1})["RRaverage2"]
    RRT = ((1 - (winrate / 100)) / (winrate / 100))

    # Calculer WinrateT
    WinrateT = (1 / (1 + risk_reward)) * 100

    # Ajouter les valeurs calculées à la collection "unitaire"
    collection_unitaire.update_one({}, {"$set": {"RRFlat": RRT, "WinrateFlat": WinrateT}}, upsert=True)
