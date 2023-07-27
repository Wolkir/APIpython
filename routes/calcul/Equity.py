from flask import Blueprint
from pymongo import MongoClient

Equity = Blueprint('Equity', __name__)

@Equity.route('/equity', methods=['GET'])
def calculate_equity(data):
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

    return data  # Return the data with the 'equity' field updated
