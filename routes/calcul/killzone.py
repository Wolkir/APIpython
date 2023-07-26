from flask import Blueprint, jsonify, request
from datetime import datetime, time

killzone = Blueprint('killzone', __name__)

def calculate_killzone(data):
    # Convertir la chaîne 'dateAndTimeOpening' en objet datetime
    opening_datetime = datetime.strptime(data['dateAndTimeOpening'], "%Y-%m-%dT%H:%M:%S.%f%z")

    # Récupérer l'heure d'ouverture de chaque document
    opening_time = opening_datetime.time()

    # Déterminer si l'heure d'ouverture se trouve dans l'une des plages horaires spécifiées
    if (time(3, 0) <= opening_time <= time(6, 0)) or (time(9, 0) <= opening_time <= time(12, 0)) or (time(14, 0) <= opening_time <= time(17, 0)):
        killzone_status = True
    else:
        killzone_status = False

    # Mettre à jour ou ajouter la clé 'killzone' dans le dictionnaire data
    data['killzone'] = killzone_status

    return data['killzone']  # Vous pouvez également retourner toute autre information que vous souhaitez utiliser ultérieurement.



