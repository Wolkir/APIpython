from flask import Blueprint
from pymongo import MongoClient

# Connexion à la base de données MongoDB
client = MongoClient('mongodb+srv://pierre:ztxiGZypi6BGDMSY@atlascluster.sbpp5xm.mongodb.net/?retryWrites=true&w=majority')
db = client['test']
collection = db['things']

RR = Blueprint('RR', __name__)

@RR.route('/rr', methods=['GET'])
def calculate_rr():
    # Récupération des documents de la collection
    documents = collection.find()

    for document in documents:
        price_close = document['priceClosure']
        price_opening = document['priceOpening']
        stop_loss = document['stopLoss']

        # Calcul de la valeur de la clé "RR"
        rr = (price_close - price_opening) + (price_opening - stop_loss)

        # Mise à jour du document avec la clé "RR"
        collection.update_one({'_id': document['_id']}, {'$set': {'RR': rr}})

    # Fermeture de la connexion à la base de données
    client.close()
    
    return 'Clé "RR" mise à jour avec succès.'
