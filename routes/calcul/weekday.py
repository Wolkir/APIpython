from flask import Flask, Blueprint, jsonify, request
from pymongo import MongoClient
from datetime import datetime

weekday = Blueprint('weekday', __name__)

@weekday.route('/weekday', methods=['GET'])
def add_weekday(data):
    client = MongoClient('mongodb+srv://pierre:ztxiGZypi6BGDMSY@atlascluster.sbpp5xm.mongodb.net/test?retryWrites=true&w=majority')
    db = client['test']

    username = data.get('username')  # Récupérer le nom d'utilisateur depuis les arguments de requête
    date_and_time_opening = data.get('dateAndTimeOpening')  # Récupérer la date et l'heure d'ouverture depuis les arguments de requête

    if not username or not date_and_time_opening:
        return "Nom d'utilisateur ou dateAndTimeOpening manquant dans les arguments de requête.", 400

    # Convertir la date et l'heure d'ouverture en objet datetime
    opening_datetime = datetime.strptime(date_and_time_opening, "%Y-%m-%dT%H:%M:%S.%f%z")

    # Obtenir le jour de la semaine en chaîne de caractères (en anglais)
    weekday_str = opening_datetime.strftime("%A")

    return str(weekday_str)
