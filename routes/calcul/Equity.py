from flask import Flask, request, jsonify, Blueprint
from pymongo import MongoClient
from functools import reduce

app = Flask(__name__)
client = MongoClient("mongodb+srv://pierre:ztxiGZypi6BGDMSY@atlascluster.sbpp5xm.mongodb.net/test?retryWrites=true&w=majority")
db = client["test"]

Equity = Blueprint('Equity', __name__)

@Equity.route('/equity', methods=['GET'])
def calculate_equity(data):
    # Get the last equity value from "test2_close" collection
    last_equity = db["test2_close"].find_one({}, sort=[('_id', -1)])['Equity']

    # Define a function to calculate the cumulative equity
    def calculate_cumulative_equity(previous_equity, document):
        if 'profit' in document:
            profit = document['profit']
            current_equity = previous_equity + profit
            document['Equity'] = current_equity
            return current_equity
        return previous_equity

    # Use reduce to calculate the cumulative equity for each document in 'data'
    final_equity = reduce(calculate_cumulative_equity, data, last_equity)

    return data

# Register the blueprint in the app
app.register_blueprint(Equity)

# Run the Flask app
if __name__ == "__main__":
    app.run()
