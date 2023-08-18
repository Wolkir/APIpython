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

    def get_best_average_for_key(key):
        total_by_key = {}
        count_by_key = {}

        for doc in collection.find():
            value = doc.get(meilleur, 0)
            key_value = doc.get(key)
            if key_value:
                total_by_key[key_value] = total_by_key.get(key_value, 0) + value
                count_by_key[key_value] = count_by_key.get(key_value, 0) + 1

        best_avg = -float("inf") 
        best_key_value = None
        for key_value, total in total_by_key.items():
            avg = total / count_by_key[key_value]
            if avg > best_avg:
                best_avg = avg
                best_key_value = key_value

        return best_key_value, best_avg

    best_day, best_day_avg = get_best_average_for_key("Day")
    best_session, best_session_avg = get_best_average_for_key("session")
    
    # ... votre code pour d'autres combinaisons ...

    response = {
        'best_day': best_day,
        'best_day_average': best_day_avg,
        'best_session': best_session,
        'best_session_average': best_session_avg
        # ... ajoutez d'autres éléments de réponse ici ...
    }
    
    # Stockage des résultats dans la nouvelle collection
    new_collection_name = f"{username}_temporaire"
    db[new_collection_name].insert_one(response)

    return jsonify(response)
