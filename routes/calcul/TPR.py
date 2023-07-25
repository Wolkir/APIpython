import requests
from flask import Blueprint, jsonify

# Connexion à la base de données MongoDB
from pymongo import MongoClient

client = MongoClient('mongodb+srv://pierre:ztxiGZypi6BGDMSY@atlascluster.sbpp5xm.mongodb.net/?retryWrites=true&w=majority')
db = client['test']
collection = db['test2_open']

tpr = Blueprint('tpr', __name__)

# Function to fetch real-time data from the API
def fetch_real_time_data():
    # Replace 'YOUR_API_URL' with the URL of the real-time data API you are using
    response = requests.get('https://apipython2.onrender.com/savetraderequest')

    # Check if the request was successful
    if response.status_code == 200:
        # Assuming the API returns data in JSON format, you can use response.json() to parse it
        data = response.json()
        return data
    else:
        print("Failed to fetch real-time data from the API.")
        return None

@tpr.route('/tpr', methods=['GET'])
def update_tpr():
    data = fetch_real_time_data()

    if data:
        for entry in data:
            type_of_transaction = entry.get('typeOfTransaction')
            price_closure = entry.get('priceClosure')
            take_profit = entry.get('takeProfit')

            print("type_of_transaction", type_of_transaction)
            print("price_closure:", price_closure)
            print("take_profit:", take_profit)

            if type_of_transaction == "buy" and price_closure >= take_profit:
                entry['TPR'] = True
            elif type_of_transaction == "sell" and price_closure <= take_profit:
                entry['TPR'] = True
            else:
                entry['TPR'] = False

            print("TPR:", entry['TPR'])

            collection.update_one({'_id': entry['_id']}, {'$set': {'TPR': entry['TPR']}})

    return jsonify({'message': 'TPR updated successfully'})

