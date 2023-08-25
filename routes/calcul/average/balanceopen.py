from flask import Flask, Blueprint, jsonify, request, abort
from pymongo import MongoClient, DESCENDING
from datetime import datetime

balanceopen = Blueprint('balanceopen', __name__)

# Connexion à la base de données MongoDB
client = MongoClient('mongodb+srv://USERNAME:PASSWORD@YOUR_URL')
db = client['test']


@balanceopen.route('/save_balance', methods=['POST'])
def save_balance(data):
    data = request.get_json()
    tradecount = data.get('tradecount')
    status = data.get('status')
    balance = data.get('balance')
    date_received = data.get('date')  # Je suppose que vous recevez aussi une date avec le format donné
    collection_name = f"{username}_temporaire"
    collection = db[collection_name]

    # Vérifier si les clés nécessaires sont présentes dans la demande
    if not all([tradecount, status, balance, date_received]):
        abort(400, 'Missing data')

    # Convertir la date reçue en objet datetime pour extraire seulement la partie jour
    date_obj = datetime.strptime(date_received, '%Y-%m-%dT%H:%M:%S.%f%z')
    current_date = date_obj.strftime('%Y-%m-%d')

    # Si c'est le premier trade ouvert du jour
    if tradecount == 1 and status == "open":
        # Vérifier si la valeur a déjà été enregistrée aujourd'hui
        existing_balance = collection.find_one({'date': current_date})
        if not existing_balance:
            collection.insert_one({'date': current_date, 'balanceopen': balance})

    return jsonify({'message': 'Data processed successfully'}), 200
