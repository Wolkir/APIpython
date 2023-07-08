from flask import Blueprint, jsonify
from pymongo import MongoClient

# Connexion à la base de données MongoDB
client = MongoClient('mongodb+srv://pierre:ztxiGZypi6BGDMSY@atlascluster.sbpp5xm.mongodb.net/?retryWrites=true&w=majority')

RRetBE = Blueprint('RRetBE', __name__)

@RRetBE.route('/RRetBE', methods=['GET'])
def calculate_rr_route():
    # Connexion à la base de données MongoDB
    db = client['test']
    collection = db['thingsTest']

    # Récupération des documents de la collection
    documents = collection.find()

    # Parcours des documents et calcul du Risk Reward
    for document in documents:
        price_close = document['priceClosure']
        price_opening = document['priceOpening']
        stop_loss = document['stopLoss']
 
        # Calcul de la valeur de la clé "RR"
        rr = (price_close - price_opening) + (price_opening - stop_loss)

        # Mise à jour du document avec la clé "RR"
        collection.update_one({'_id': document['_id']}, {'$set': {'RR': rr}})

    # Vérification du Risk Reward et calcul du Break Even
    check_risk_reward()

    # Fermeture de la connexion à la base de données
    client.close()
    
    return jsonify({'message': 'Risk Reward and Break Even calculated successfully'})

def check_risk_reward():
    # Connexion à la base de données MongoDB
    db = client['test']
    collection = db['things']

    # Récupération des données de la collection things
    data = list(collection.find())

    # Parcours des données et vérification du Risk Reward
    for entry in data:
        break_even = entry.get('breakEven')
        risk_reward = entry.get('RR')

        if risk_reward is not None and break_even is not None:
            if -0.5 < risk_reward < 0.5 and break_even > risk_reward:
                entry['RR_check'] = True
            else:
                entry['RR_check'] = False
        else:
            entry['RR_check'] = False

        # Mise à jour du document dans la collection things
        collection.update_one({'_id': entry['_id']}, {'$set': {'RR_check': entry['RR_check']}})
