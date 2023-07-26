from flask import Flask, Blueprint, jsonify, request
from datetime import datetime

session = Blueprint('session', __name__)

@session.route('/session', methods=['POST'])
def determine_session():
    data = request.json  # Récupérer les données JSON de la requête

    # Parcourir tous les documents pour déterminer la session en fonction de l'heure d'ouverture
    for doc in data:
        # Vous pouvez ajuster le format d'heure ici en fonction de celui dans votre requête JSON
        # Par exemple, si le format est "%Y-%m-%dT%H:%M:%S.%f%z", utilisez :
        # opening_time = datetime.strptime(doc['dateAndTimeOpening'], "%Y-%m-%dT%H:%M:%S.%f%z")
        opening_time = datetime.strptime(doc['dateAndTimeOpening'], "%Y-%m-%d %H:%M:%S.%f")

        # Déterminer la session en fonction de l'heure d'ouverture
        if opening_time.hour >= 0 and opening_time.hour < 7:
            session = "AS"
        elif opening_time.hour >= 8 and opening_time.hour < 12:
            session = "LD"
        elif opening_time.hour >= 13 and opening_time.hour < 15:
            session = "NY"
        else:
            session = "ND"

        # Ajouter la session au document actuel
        doc['session'] = session

    return jsonify(data)  # Retourner les données JSON mises à jour avec la clé 'session'

