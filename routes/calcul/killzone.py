from flask import Blueprint, jsonify, request
from datetime import time

#killzone_blueprint = Blueprint('killzone', __name__)
killzone = Blueprint('killzone', __name__)
data = request.json
#@killzone_blueprint.route('/killzone', methods=['POST'])
def calculate_killzone(data):
  
    results = []

    # Parcourir tous les documents de la collection
    for doc in data:
        # Récupérer l'heure d'ouverture de chaque document
        opening_time = datetime.strptime(data['dateAndTimeOpening'], "%Y.%m.%d %H:%M:%S.%f").time()

        # Déterminer si l'heure d'ouverture se trouve dans l'une des plages horaires spécifiées
        if (time(3, 0) <= opening_time <= time(6, 0)) or (time(9, 0) <= opening_time <= time(12, 0)) or (time(14, 0) <= opening_time <= time(17, 0)):
            killzone_status = True
        else:
            killzone_status = False
       
        return killzone_status


