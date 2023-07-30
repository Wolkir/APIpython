from flask import Flask, Blueprint, jsonify
from pymongo import MongoClient
from datetime import timedelta

app = Flask(__name__)
averagegainloss = Blueprint('averagegainloss', __name__)

# Connexion à la base de données MongoDB
client = MongoClient('mongodb+srv://pierre:ztxiGZypi6BGDMSY@atlascluster.sbpp5xm.mongodb.net/?retryWrites=true&w=majority')
db = client['test']

@averagegainloss.route('/averagegainloss', methods=['GET'])

def calculate_average_gain_loss_rr(data):
    username = data.get('username')
    collection_name = f"{username}_close"
    collection_unitaire = f"{username}_unitaire"
    collection = db[collection_name]
  
    # Initialisation des variables
    positive_gains_total = 0
    positive_gains_count = 0
    positive_ticket_numbers = set()

    negative_losses_total = 0
    negative_losses_count = 0
    negative_ticket_numbers = set()

    rr_values = []  # Liste pour stocker les valeurs de RR

    # Parcourir les documents de la collection
    for doc in collection.find():
        profit = doc['profit']
        ticket_number = doc['ticketNumber']
        
        if profit > 0 and ticket_number not in positive_ticket_numbers:
            positive_gains_total += profit
            positive_gains_count += 1
            positive_ticket_numbers.add(ticket_number)
        
        elif profit < 0 and ticket_number not in negative_ticket_numbers:
            negative_losses_total += profit
            negative_losses_count += 1
            negative_ticket_numbers.add(ticket_number)

      for document in collection.find():
          if "RR" in document:
              rr_values.append(document["RR"])
              
    

        

    # Calcul de la moyenne des gains et pertes
    average_gain = positive_gains_total / positive_gains_count if positive_gains_count > 0 else 0
    average_loss = negative_losses_total / negative_losses_count if negative_losses_count > 0 else 0

    # Calcul de la moyenne des valeurs de RR
    rr_total = sum(rr_values)
    rr_count = len(rr_values)
    average_rr = rr_total / rr_count if rr_count > 0 else 0

    # Calculer la durée moyenne
    total_duration = timedelta()
    document_count = 0

    for doc in collection.find():
        if 'duration' in doc:
            duration_str = doc['duration']
            duration_parts = duration_str.split(':')
            duration = timedelta(hours=int(duration_parts[0]), minutes=int(duration_parts[1]), seconds=int(duration_parts[2]))
            total_duration += duration
            document_count += 1

    average_duration = total_duration / document_count if document_count > 0 else timedelta()

    # Insérer les valeurs dans la collection "unitaire"
    unitaire_collection = db[collection_unitaire]
    unitaire_collection.update_one(
        {},
        {
            '$set': {
                'averagegain2': average_gain,
                'averagelosse2': average_loss,
                'RRaverage2': average_rr,
                'average_duration2': str(average_duration)
            }
        },
        upsert=True
    )

