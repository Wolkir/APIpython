from flask import Blueprint, jsonify, request
from datetime import datetime

session = Blueprint('session', __name__)

def determine_session(data):
    # Parcourir tous les documents pour déterminer la session en fonction de l'heure d'ouverture
    for doc in data:
        # Vous pouvez ajuster le format d'heure ici en fonction de celui dans votre requête JSON
        # Par exemple, si le format est "%Y-%m-%dT%H:%M:%S.%f%z", utilisez :
        # opening_time = datetime.strptime(doc['dateAndTimeOpening'], "%Y-%m-%dT%H:%M:%S.%f%z")
        opening_time = datetime.strptime(doc['dateAndTimeOpening'], "%Y-%m-%d %H:%M:%S.%f")

        # Déterminer la session en fonction de l'heure d'ouverture
        if opening_time.hour >= 0 and opening_time.hour < 7:
            session_value = "AS"
        elif opening_time.hour >= 8 and opening_time.hour < 12:
            session_value = "LD"
        elif opening_time.hour >= 13 and opening_time.hour < 15:
            session_value = "NY"
        else:
            session_value = "ND"

        # Mettre à jour ou ajouter la clé 'session' dans le dictionnaire data
        doc['session'] = session_value

    return session_value


