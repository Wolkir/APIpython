from flask import Blueprint, jsonify
from pymongo import MongoClient

# Connexion à la base de données MongoDB
client = MongoClient('mongodb+srv://pierre:ztxiGZypi6BGDMSY@atlascluster.sbpp5xm.mongodb.net/?retryWrites=true&w=majority')

BE = Blueprint('BE', __name__)

@BE.route('/BE', methods=['GET'])
def update_BE():
    # Connexion à la base de données MongoDB
    client = MongoClient('mongodb+srv://pierre:ztxiGZypi6BGDMSY@atlascluster.sbpp5xm.mongodb.net/?retryWrites=true&w=majority')
    db = client['test']
    collection = db['thingsTest']

    # Récupération des données de la collection things
    data = list(collection.find())

    # Parcours des données et vérification du Risk Reward
    for entry in data:
        rr = entry.get('RR')

        if -0.5 < rr < 0.5:
            entry['BE'] = True
        else:
            entry['BE'] = False

        # Mise à jour du document dans la collection things
        collection.update_one({'_id': entry['_id']}, {'$set': {'BE': entry['BE']}})

    # Fermeture de la connexion à la base de données
    client.close()

    return jsonify({'message': 'BE checked successfully'})
