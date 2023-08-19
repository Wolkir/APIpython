from flask import Flask, Blueprint, jsonify, request
from pymongo import MongoClient

app = Flask(__name__)
bestrr = Blueprint('bestrr', __name__)

# Connexion à la base de données MongoDB
client = MongoClient('mongodb+srv://pierre:ztxiGZypi6BGDMSY@atlascluster.sbpp5xm.mongodb.net/?retryWrites=true&w=majority')
db = client['test']

@bestrr.route('/best', methods=['GET'])
def calculate_best_rr():
    collection_name = request.args.get('collection', None)
    username = request.args.get('username', None)
    meilleur = request.args.get('meilleur', None)
    
    collection = db[collection_name]
    
    def get_best_for_key(key):
        count_by_key = {}
        total_by_key = {}
        first_value = collection.find_one().get(meilleur, None)
        
        if isinstance(first_value, bool):  # Si la première valeur est un booléen
            for doc in collection.find():
                value = doc.get(meilleur, False)
                key_value = doc.get(key)
                if value:
                    count_by_key[key_value] = count_by_key.get(key_value, 0) + 1
                    
            max_count = -1
            best_key_value = None
            for key, count in count_by_key.items():
                if count > max_count:
                    max_count = count
                    best_key_value = key
                    
            return best_key_value, max_count  # on retourne le nombre de `True` pour la meilleure clé
        
        else:  # Sinon, on suppose que c'est une valeur numérique et on calcule une moyenne
            for doc in collection.find():
                value = doc.get(meilleur, 0)
                key_value = doc.get(key)
                total_by_key[key_value] = total_by_key.get(key_value, 0) + value
                count_by_key[key_value] = count_by_key.get(key_value, 0) + 1
            
            best_avg = -float("inf")
            best_key_value = None
            for key_value, total in total_by_key.items():
                avg = total / count_by_key[key_value]
                if avg > best_avg:
                    best_avg = avg
                    best_key_value = key_value
                    
            return best_key_value, best_avg  # on retourne la moyenne pour la meilleure clé
    
    # Utilisez la fonction pour chaque clé
    best_symbol, best_symbol_value = get_best_for_key('symbol')
    best_orderType, best_orderType_value = get_best_for_key('orderType')
    best_day, best_day_value = get_best_for_key('Day')
    best_session, best_session_value = get_best_for_key('session')
    # ... ajoutez d'autres clés si nécessaire

    response = {
        'best_symbol': best_symbol,
        'best_symbol_value': best_symbol_value,
        'best_orderType': best_orderType,
        'best_orderType_value': best_orderType_value,
        'best_day': best_day,
        'best_day_value': best_day_value,
        'best_session': best_session,
        'best_session_value': best_session_value
        # ... ajoutez d'autres clés si nécessaire
    }

    # Stockage des résultats dans la nouvelle collection
    new_collection_name = f"{username}_temporaire"
    db[new_collection_name].insert_one(response)

    return jsonify(response)
