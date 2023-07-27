from flask import Blueprint, request, jsonify
from pymongo import MongoClient

Equity = Blueprint('Equity', __name__)

def calculate_equity(data):
    # Initialize a variable to store the previous equity value
    previous_equity = 0.0  # Utiliser 0.0 pour indiquer que c'est un nombre à virgule flottante

    try:
        profit = data['profit']

        # Calculate the new equity value by adding the previous equity and the current profit
        equity = previous_equity + profit

        # Update the data entry with the new equity value
        data['equity'] = str(equity)

        return data  # Renvoyer la nouvelle équité sous forme de nombre à virgule flottante
    except Exception as e:
        return {"error": str(e)}  # Return an error response if an exception occurs
