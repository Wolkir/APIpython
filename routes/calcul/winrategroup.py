from flask import Flask, Blueprint, jsonify
from pymongo import MongoClient

winrategroup = Blueprint('winrategroup', __name__)

# Connexion à la base de données MongoDB
client = MongoClient('mongodb+srv://pierre:ztxiGZypi6BGDMSY@atlascluster.sbpp5xm.mongodb.net/?retryWrites=true&w=majority')
db = client['test']

@winrategroup.route('/winrategroup', methods=['GET'])
def calculate_winrate_group(data):
    username = request.args.get('username')
    identifier = request.args.get('identifier')
    collection_name = f"{username}_close"
    collection_unitaire = f"{username}_unitaire"
    collection = db[collection_name]
    
    # Récupérer tous les documents
    documents = list(collection.find())
    
    # Fonction pour calculer le winrate
    def calculate_winrate(documents, order_type):
        positive_profits_count = 0
        positive_identifiers = set()

        for doc in documents:
            profit = doc['profit']
            order_type_doc = doc['orderType']
            identifier = doc['identifier']
            
            if order_type_doc == order_type and profit > 0 and identifier not in positive_identifiers:
                positive_profits_count += 1
                positive_identifiers.add(identifier)

        return positive_profits_count / len(positive_identifiers) * 100

    # Calcul du winrate standard pour tous les ordres
    positive_profits_count_buy = calculate_winrate(documents, "BUY")
    positive_profits_count_sell = calculate_winrate(documents, "SELL")
    winratestd = positive_profits_count_buy + positive_profits_count_sell
    
    # Compter le nombre de documents avec profit > 0 pour le calcul du winrate real
    positive_profits_count_real = collection.count_documents({"profit": {"$gt": 0}})
    
    # Compter le nombre de documents avec profit < 0 pour le calcul du winrate real
    negative_profits_count_real = collection.count_documents({"profit": {"$lt": 0}})
    
    # Calcul du winrate real
    winrate_value_real = positive_profits_count_real / (positive_profits_count_real + negative_profits_count_real) * 100

    # Insérer les winrates dans la collection "unitaire"
    unitaire_collection = db[collection_unitaire]
    unitaire_collection.update_one({}, {
        '$set': {
            'winratestdl': winratestd,
            'winratereal': winrate_value_real,
            'winratestd_buy': positive_profits_count_buy,
            'winratestd_sell': positive_profits_count_sell
        }
    }, upsert=True)



