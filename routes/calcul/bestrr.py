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
    
    collection = db[collection_name]  # Utilisation du nom de la collection pour interroger la BD

    best_rr = 0
    best_day = ""
    best_symbol = ""
    best_order_type = ""

    meilleur_by_combination = {}
    meilleur_count_combination = {}

    for doc in collection.find():
        rr_value = doc.get('RR', 0)
        #day = doc.get('Day')
        symbol = doc.get('symbol')
        order_type = doc.get('orderType')
        combination = (symbol, order_type)

        if rr_value is not None:
            meilleur_by_combination[combination] =  meilleur_by_combination.get(combination, 0) + rr_value
            meilleur_count_combination[combination] = meilleur_count_combination.get(combination, 0) + 1

    for combination, rr_total in meilleur_by_combination.items():
        rr_count = meilleur_count_combination.get(combination, 0)
        average_rr = rr_total / rr_count if rr_count > 0 else 0

        if average_rr > best_rr:
            best_rr = average_rr
            best_symbol, best_order_type = combination

    response = {
        'best_symbol': best_symbol,
        'best_order_type': best_order_type,
        'best_rr': best_rr
    }

    # Stockage des résultats dans la nouvelle collection
    new_collection_name = f"{username}_temporaire"
    db[new_collection_name].insert_one(response)

    return jsonify(response)

app.register_blueprint(bestrr, url_prefix='/bestrr')

if __name__ == '__main__':
    app.run()
