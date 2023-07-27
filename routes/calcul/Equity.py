from flask import Blueprint, request, jsonify
from pymongo import MongoClient


client = MongoClient("mongodb+srv://pierre:ztxiGZypi6BGDMSY@atlascluster.sbpp5xm.mongodb.net/test?retryWrites=true&w=majority")
db = client["test"]
Equity = Blueprint('Equity', __name__)
def calculate_equity(data):
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

        # Ajouter la nouvelle valeur d'équité à la variable Equity dans l'objet data
        data['Equity'] = equity

        return data  # Renvoyer l'objet data avec la nouvelle équité ajoutée
    except Exception as e:
        return {"error": str(e)}  # Renvoyer une réponse d'erreur en cas d'exception
