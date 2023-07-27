from flask import Blueprint, request, jsonify
from pymongo import MongoClient

Equity = Blueprint('Equity', __name__)

@Equity.route('/equity', methods=['POST'])
def calculate_equity(data):
    data = request.json  # Assuming you are sending data in JSON format through the request

    # Initialize a variable to store the previous equity value
    previous_equity = 0

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

    return jsonify(data)  # Return the updated data as a JSON response


