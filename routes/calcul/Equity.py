from flask import Flask, request, jsonify, Blueprint
from pymongo import MongoClient

app = Flask(__name__)
client = MongoClient("mongodb+srv://pierre:ztxiGZypi6BGDMSY@atlascluster.sbpp5xm.mongodb.net/test?retryWrites=true&w=majority")
db = client["test"]

Equity = Blueprint('Equity', __name__)

@Equity.route('/equity', methods=['GET'])
def calculate_equity(data):
    # Get the last equity value from "test2_close" collection
    last_equity = db["test2_close"].find_one({}, sort=[('_id', -1)])['equity']

    # Calculate new equity for each document in 'data'
    for document in data:
        if 'profit' in document:
            profit = document['profit']
            last_equity += profit
            document['equity'] = last_equity

    return jsonify(data)

# Register the blueprint in the app
app.register_blueprint(Equity)

# Run the Flask app
if __name__ == "__main__":
    app.run()
