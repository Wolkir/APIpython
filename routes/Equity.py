from flask import Blueprint
from pymongo import MongoClient

Equity = Blueprint('Equity', __name__)

@Equity.route('/equity', methods=['GET'])
def calculate_equity():
    # Connexion à la base de données MongoDB
    client = MongoClient('mongodb+srv://pierre:ztxiGZypi6BGDMSY@atlascluster.sbpp5xm.mongodb.net/?retryWrites=true&w=majority')
    db = client['test']
    collection = db['things']

    # Récupération des documents de la collection
    documents = collection.find()

    previous_equity = 0  # Variable to store the previous equity value

    for document in documents:
        if 'profit' in document:
            profit = document['profit']

            # Calculate the new equity value by adding the previous equity and the current volume
            equity = previous_equity + profit

            # Update the document with the new equity value
            collection.update_one({'_id': document['_id']}, {'$set': {'equity': equity}})

            previous_equity = equity  # Update the previous equity value for the next iteration

    # Fermeture de la connexion à la base de données
    client.close()

    return 'Clé "profsdit" mise à jour avec succès.'
