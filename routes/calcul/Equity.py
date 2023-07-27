from flask import Blueprint, request, jsonify
from pymongo import MongoClient

Equity = Blueprint('Equity', __name__)

def calculate_equity(username, data):
    try:
        # Récupérer la dernière valeur d'équité de la collection username_close
        collection_name = f"{username}_close"
        collection = db[collection_name]
        last_entry = collection.find_one(sort=[('_id', -1)])
        previous_equity = last_entry.get('equity', 0.0)

        # Récupérer la valeur de profit depuis l'objet data
        profit = data.get('profit', 0.0)

        # Calculer la nouvelle valeur d'équité
        equity = previous_equity + profit

        # Insérer la nouvelle valeur d'équité dans la collection
        collection.insert_one({'equity': equity})

        return equity  # Renvoyer la nouvelle équité sous forme de nombre à virgule flottante
    except Exception as e:
        return {"error": str(e)}  # Renvoyer une réponse d'erreur en cas d'exception
