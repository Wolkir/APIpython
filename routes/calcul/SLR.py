from flask import Blueprint, jsonify, request
from pymongo import MongoClient

# Connexion à la base de données MongoDB
client = MongoClient('mongodb+srv://pierre:ztxiGZypi6BGDMSY@atlascluster.sbpp5xm.mongodb.net/?retryWrites=true&w=majority')

slr = Blueprint('slr', __name__)

def calculate_slr(entry):
    # Your SLR calculation logic here based on the 'entry' data
    # For example:
    type_of_transaction = entry.get('typeOfTransaction')
    price_closure = entry.get('priceClosure')
    stop_loss = entry.get('stopLoss')

    if type_of_transaction == "Buy" and price_closure <= stop_loss:
        entry['SLR'] = True
    elif type_of_transaction == "Sell" and price_closure >= stop_loss:
        entry['SLR'] = True
    else:
        entry['SLR'] = False

    return entry

@slr.route('/slr', methods=['POST'])
def update_slr():
    try:
        data = request.json

        for entry in data:
            # Calculate the SLR value for each entry
            entry = calculate_slr(entry)

            # Update the entry in the database with the SLR value
            db = client['test']
            collection = db['test2_open']
            collection.update_one({'_id': entry['_id']}, {'$set': {'SLR': entry['SLR']}})
        
        return jsonify({'message': 'SLR updated successfully'}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400
