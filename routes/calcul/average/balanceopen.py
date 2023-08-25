from flask import Flask, Blueprint, jsonify, request, abort
from pymongo import MongoClient, DESCENDING
from datetime import datetime

balanceopen = Blueprint('balanceopen', __name__)

# Connexion à la base de données MongoDB
client = MongoClient('mongodb+srv://pierre:ztxiGZypi6BGDMSY@atlascluster.sbpp5xm.mongodb.net/?retryWrites=true&w=majority')
db = client['test']

@balanceopen.route('/save_balance', methods=['POST'])
def save_balance(data):
    username = data.get('username')
    tradecount = data.get('tradecount')
    closurePosition  = data.get('closurePosition')
    balance = data.get('balance')
    date = data.get('dateAndTimeOpening')  # Je suppose que vous recevez aussi une date avec le format donné
    collection_name = f"{username}_temporaire"
    collection = db[collection_name]

    # Vérifier si les clés nécessaires sont présentes dans la demande
    if not all([tradecount, closurePosition, balance,date]):
        abort(400, 'Missing data')

    # Convertir la date reçue en objet datetime pour extraire seulement la partie jour
    date_obj = datetime.strptime(date, '%Y-%m-%dT%H:%M:%S.%f%z')
    current_date = date_obj.strftime('%Y-%m-%d')

    # Si c'est le premier trade ouvert du jour
    if tradecount == 1 and closurePosition == "open":
        # Vérifier si la valeur a déjà été enregistrée aujourd'hui
        existing_balance = collection.find_one({'date': current_date})
        if not existing_balance:
            collection.insert_one({'date': current_date, 'balanceopen': balance})

    return jsonify({'message': 'Data processed successfully'}), 200
