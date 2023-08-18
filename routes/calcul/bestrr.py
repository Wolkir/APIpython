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

    best_value = 0  # Remplacé best_rr par best_value pour généralisation
    best_symbol = ""
    best_order_type = ""
    best_day=""
    best_session=""
    
    total_by_combination = {}  # Renommé pour la clarté
    count_combination = {}

    for doc in collection.find():
        variable_value = doc.get(meilleur, 0)  # Utilisez la valeur de 'meilleur' comme clé
        symbol = doc.get('symbol')
        order_type = doc.get('orderType')
        day = doc.get('Day')
        session=doc.get('session')
        combination = (symbol, order_type,day,session)

        total_by_combination[combination] =  total_by_combination.get(combination, 0) + variable_value
        count_combination[combination] = count_combination.get(combination, 0) + 1

    for combination, total_value in total_by_combination.items():
        count_value = count_combination.get(combination, 0)
        average_value = total_value / count_value if count_value > 0 else 0

        if average_value > best_value:
            best_value = average_value
            best_symbol, best_order_type, best_day, best_session = combination

    response = {
        'best_symbol': best_symbol,
        'best_order_type': best_order_type,
        'best_day': best_day
        'best_session': best_session
        'best_value': best_value  # Remplacé best_rr par best_value
    }

    # Stockage des résultats dans la nouvelle collection
    new_collection_name = f"{username}_temporaire"
    db[new_collection_name].insert_one(response)

    return jsonify(response)

app.register_blueprint(bestrr, url_prefix='/bestrr')

if __name__ == '__main__':
    app.run()
