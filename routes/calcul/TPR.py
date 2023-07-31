from flask import Blueprint, jsonify, request
from pymongo import MongoClient

# Connexion à la base de données MongoDB
client = MongoClient('mongodb+srv://pierre:ztxiGZypi6BGDMSY@atlascluster.sbpp5xm.mongodb.net/?retryWrites=true&w=majority')

tpr = Blueprint('tpr', __name__)

def calculate_tpr(entry):
    # Your TPR calculation logic here based on the 'entry' data
    # For example:
    orderType = entry.get('orderType')
    price_closure = entry.get('priceClosure')
    take_profit = entry.get('takeProfit')
    
    if orderType == "BUY" and price_closure >= take_profit and take_profit>0:
        entry['TPR'] = True
    elif orderType == "SELL" and price_closure <= take_profit and take_profit>0 :
        entry['TPR'] = True
    else:
        entry['TPR'] = False

    return entry


@tpr.route('/tpr', methods=['POST'])
def update_tpr():
    try:
        data = request.json

        for entry in data:
            # Calculate the TPR value for each entry
            entry = calculate_tpr(entry)

            # Update the entry in the database with the TPR value
            db = client['test']
            collection = db['test2_open']
            collection.update_one({'_id': entry['_id']}, {'$set': {'TPR': entry['TPR']}})
        
        return jsonify({'message': 'TPR updated successfully'}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400
