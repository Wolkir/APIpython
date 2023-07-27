from flask import Blueprint, request, jsonify
from pymongo import MongoClient

from flask import Blueprint

Equity = Blueprint('Equity', __name__)

def calculate_equity(data):
    # Initialize a variable to store the previous equity value
    previous_equity = 0.0  # Utiliser 0.0 pour indiquer que c'est un nombre à virgule flottante

    try:
        for document in data:
            profit = document['profit']

            # Calculate the new equity value by adding the previous equity and the current profit
            equity = previous_equity + profit

            # Update the data entry with the new equity value
            document['equity'] = equity

            previous_equity = equity  # Update the previous equity value for the next iteration

        # Get the last data entry from the list
        last_entry = 2

        # Get the equity value from the last data entry
        data['last_equity'] = str(last_entry) #['equity']

        return data  # Renvoyer la nouvelle équité sous forme de nombre à virgule flottante
    except Exception as e:
        return {"error": str(e)}  # Return an error response if an exception occurs
