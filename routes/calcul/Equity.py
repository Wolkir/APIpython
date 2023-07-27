from flask import Blueprint, request, jsonify
from pymongo import MongoClient

from flask import Blueprint

Equity = Blueprint('Equity', __name__)

@Equity.route('/equity', methods=['GET'])
def calculate_equity(data):
    # Initialize a variable to store the previous equity value
    previous_equity = 0.0  # Utiliser 0.0 pour indiquer que c'est un nombre à virgule flottante

    # Iterate over each data entry
    for document in data:
        if 'profit' in document:
            profit = document['profit']

            # Calculate the new equity value by adding the previous equity and the current profit
            equity = previous_equity + profit

            # Update the data entry with the new equity value
            document['equity'] = equity

            previous_equity = equity  # Update the previous equity value for the next iteration

    # Get the last data entry from the list
    last_entry = data[-1]

    # Get the equity value from the last data entry
    last_equity = last_entry['equity']

    return last_equity  # Renvoyer la nouvelle équité sous forme de nombre à virgule flottante
