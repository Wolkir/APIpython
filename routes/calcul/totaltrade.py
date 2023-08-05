from flask import Flask, Blueprint, request
from pymongo import MongoClient
from datetime import timedelta

app = Flask(__name__)
totaltrade = Blueprint('totaltrade', __name__)

# Connexion à la base de données MongoDB
client = MongoClient('mongodb+srv://pierre:ztxiGZypi6BGDMSY@atlascluster.sbpp5xm.mongodb.net/?retryWrites=true&w=majority')
db = client['test']

@totaltrade.route('/totaltrade', methods=['POST'])
def calculate_totaltrade():
    data = request.get_json()
    username = data.get('username')
    collection_name = f"{username}_close"
    collection = db[collection_name]

    last_trade = collection.find().sort('date', pymongo.DESCENDING).limit(1).to_list(length=1)

    if len(last_trade) == 0:  # if the collection is empty
        totaltrade = 1
    else:
        totaltrade = last_trade[0]['totaltrade'] + 1

    new_trade = data.get('trade')  # get the new trade from the request data
    new_trade['totaltrade'] = totaltrade  # set the totaltrade field for the new trade

    collection.insert_one(new_trade)  # insert the new trade into the collection

    return str(totaltrade), 201  # return the totaltrade value as a string

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

    # Obtenir le dernier trade de la collection triée par ordre chronologique
    last_trade = collection.find_one(sort=[('timestamp', -1)])

    # Compter le nombre total de trades dans la collection
    total_trades = collection.count_documents({})

    if total_trades == 0:
        # Aucun trade dans la collection, le numéro de position sera 1
        total_trades = 1
    else:
        # Récupérer la valeur de totaltrade du dernier trade et ajouter 1 pour le nouveau trade
        total_trades = last_trade.get('totaltrade', 0) + 1

    # Ajouter le numéro de position pour le nouveau trade ajouté à la collection
    # Au lieu de mettre à jour le dernier trade, vous devriez probablement ajouter un nouveau trade ici.
    new_trade = {"totaltrade": total_trades, "other_fields": "other_values"} # remplacez "other_fields" et "other_values" par les champs réels du nouveau trade
    collection.insert_one(new_trade)

    return jsonify({'message': 'Numéro de position ajouté à chaque trade avec succès.'})
