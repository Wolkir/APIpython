from flask import Flask, Blueprint, jsonify
from pymongo import MongoClient
from datetime import timedelta

app = Flask(__name__)
totaltrade = Blueprint('totaltrade', __name__)

# Connexion à la base de données MongoDB
client = MongoClient('mongodb+srv://pierre:ztxiGZypi6BGDMSY@atlascluster.sbpp5xm.mongodb.net/?retryWrites=true&w=majority')
db = client['test']

@totaltrade.route('/totaltrade', methods=['GET'])
def calculate_totaltrade(data):

    username = data.get('username')
    collection_name = f"{username}_close"
    collection_unitaire = f"{username}_unitaire"
    collection = db[collection_name]

    # Obtenir tous les trades de la collection triée par ordre chronologique
    trades = list(collection.find().sort('timestamp', 1))

    # Si la collection est vide, retourner un message
    if not trades:
        return jsonify({'message': 'Aucun trade dans la collection.'})

    # La première trade aura toujours totaltrade égal à 1
    trades[0]['totaltrade'] = 1

    # Calculer le totaltrade pour les trades suivants
    for i in range(1, len(trades)):
        trades[i]['totaltrade'] = trades[i-1]['totaltrade'] + 1

    # Mettre à jour tous les trades dans la collection
    for trade in trades:
        collection.update_one({'_id': trade['_id']}, {'$set': trade})

    return jsonify({'message': 'Numéro de position ajouté à chaque trade avec succès.'})

if __name__ == "__main__":
    app.run(debug=True)
