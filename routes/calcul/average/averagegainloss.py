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

    positivelong_gains_total = 0
    positivelong_gains_count = 0
    positivelong_ticket_numbers = set()

    positiveshort_gains_total = 0
    positiveshort_gains_count = 0
    positiveshort_ticket_numbers = set()

    negative_losses_total = 0
    negative_losses_count = 0
    negative_ticket_numbers = set()

    negativelong_losses_total = 0
    negativelong_losses_count = 0
    negativelong_ticket_numbers = set()

    negativeshort_losses_total = 0
    negativeshort_losses_count = 0
    negativeshort_ticket_numbers = set()

    rr_values_long = [] 
    rr_values_short = []

    # Parcourir les documents de la collection
    for doc in collection.find():
        profit = doc['profit']
        ticket_number = doc['ticketNumber']
        typeofTransaction = doc['orderType']
        
        if profit > 0 and ticket_number not in positive_ticket_numbers:
            positive_gains_total += profit
            positive_gains_count += 1
            positive_ticket_numbers.add(ticket_number)

        if profit > 0 and typeofTransaction == "BUY" and ticket_number not in positivelong_ticket_numbers:
            positivelong_gains_total += profit
            positivelong_gains_count += 1
            positivelong_ticket_numbers.add(ticket_number)

        if profit > 0 and typeofTransaction == "SELL" and ticket_number not in positiveshort_ticket_numbers:
            positiveshort_gains_total += profit
            positiveshort_gains_count += 1
            positiveshort_ticket_numbers.add(ticket_number)
        
        if profit < 0 and ticket_number not in negative_ticket_numbers:
            negative_losses_total += profit
            negative_losses_count += 1
            negative_ticket_numbers.add(ticket_number)

        if profit < 0 and typeofTransaction == "BUY" and ticket_number not in negativelong_ticket_numbers:
            negativelong_losses_total += profit
            negativelong_losses_count += 1
            negativelong_ticket_numbers.add(ticket_number)

        if profit < 0 and typeofTransaction == "SELL" and ticket_number not in negativeshort_ticket_numbers:
            negativeshort_losses_total += profit
            negativeshort_losses_count += 1
            negativeshort_ticket_numbers.add(ticket_number)

        if "RR" in doc:
            rr_value = doc["RR"]
            if typeofTransaction == "BUY":
                rr_values_long.append(rr_value)
            elif typeofTransaction == "SELL":
                rr_values_short.append(rr_value)

    # Calcul de la moyenne des gains et pertes
    average_gain = positive_gains_total / positive_gains_count if positive_gains_count > 0 else 0
    average_loss = negative_losses_total / negative_losses_count if negative_losses_count > 0 else 0
    averagelong_gain = positivelong_gains_total / positivelong_gains_count if positivelong_gains_count > 0 else 0
    averagelong_loss = negativelong_losses_total / negativelong_losses_count if negativelong_losses_count > 0 else 0
    averageshort_gain = positiveshort_gains_total / positiveshort_gains_count if positiveshort_gains_count > 0 else 0
    averageshort_loss = negativeshort_losses_total / negativeshort_losses_count if negativeshort_losses_count > 0 else 0

   # Calcul de la moyenne des valeurs de RR
    rr_total = sum(rr_values)
    rr_count = len(rr_values)
    average_rr = rr_total / rr_count if rr_count > 0 else 0

    # Pour mediane_gain
    sorted_positive_gains = sorted([profit for profit in rr_values_long if profit > 0])
    positive_gains_count = len(sorted_positive_gains)
    mediane_gain = sorted_positive_gains[positive_gains_count // 2] if positive_gains_count > 0 else 0

    # Calcul de la moyenne des valeurs de RR pour les transactions de type "BUY"
    rr_total_long = sum(rr_values_long)
    rr_count_long = len(rr_values_long)
    average_rrlong = rr_total_long / rr_count_long if rr_count_long > 0 else 0

    # Calcul de la médiane
    # Pour mediane_rrlong
    sorted_rrlong = sorted(rr_values_long)
    rr_count_long = len(sorted_rrlong)
    median_rrlong = (sorted_rrlong[rr_count_long // 2 - 1] + sorted_rrlong[rr_count_long // 2]) / 2 if rr_count_long % 2 == 0 else sorted_rrlong[rr_count_long // 2]


  
    # Calcul de la moyenne des valeurs de RR pour les transactions de type "SELL"
    rr_total_short = sum(rr_values_short)
    rr_count_short = len(rr_values_short)
    average_rrshort = rr_total_short / rr_count_short if rr_count_short > 0 else 0

    # Pour mediane_rrshort
    sorted_rrshort = sorted(rr_values_short)
    rr_count_short = len(sorted_rrshort)
    median_rrshort = (sorted_rrshort[rr_count_short // 2 - 1] + sorted_rrshort[rr_count_short // 2]) / 2 if rr_count_short % 2 == 0 else sorted_rrshort[rr_count_short // 2]
  
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
                'averagegain': average_gain,
                'mediane_gain' : mediane_gain,
                'RRaverage': average_rr,
                'averageloss': average_loss,
                'averagelonggain': averagelong_gain,
                'averagelongloss': averagelong_loss,
                'averageshortgain': averageshort_gain,
                'averageshortloss': averageshort_loss,
                'averagelong_rr': average_rrlong,
                'median_long': median_rrlong,
                'averageshort_rr': average_rrshort,
                'median_rrshort': median_rrshort,
                'average_duration': str(average_duration)
            }
        },
        upsert=True
    )
