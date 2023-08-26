from flask import Flask, Blueprint, jsonify
from pymongo import MongoClient

from datetime import datetime

tilt = Blueprint('tilt', __name__)

# Connexion à la base de données MongoDB
client = MongoClient('mongodb+srv://pierre:ztxiGZypi6BGDMSY@atlascluster.sbpp5xm.mongodb.net/?retryWrites=true&w=majority')
db = client['test']
@tilt.route('/tilt', methods=['GET'])
def find_tilt(data):
    username = data.get('username')
    equity = data.get('Equity')
    date = data.get('dateAndTimeOpening') # Je suppose que la date est aussi fournie

    if not all([username, equity, date]):
        return "Missing data", 400

    # Convertir la date reçue en objet datetime pour extraire seulement la partie jour
    date_obj = datetime.strptime(date, '%Y-%m-%dT%H:%M:%S.%f%z')
    current_date = date_obj.strftime('%Y-%m-%d')

    collection_name = f"{username}_temporaire"
    collection = db[collection_name]

    # Récupérer la valeur de `balanceopen` pour la journée
    balance_record = collection.find_one({'date': current_date})
    if not balance_record:
        return "Opening balance not found", 400
    
    opening_balance = balance_record.get('balanceopen')

    # Calculer le pourcentage de changement
    percent_change = ((equity - opening_balance) / opening_balance) * 100

    # Vérifier si le changement est inférieur à -2% et renvoyer True ou False
    if percent_change < -2:
        tilt_status = True
    else:
        tilt_status = False

    return tilt_status
