from flask import Blueprint, jsonify, request
from pymongo import MongoClient

# Connexion à la base de données MongoDB
client = MongoClient('mongodb+srv://pierre:ztxiGZypi6BGDMSY@atlascluster.sbpp5xm.mongodb.net/?retryWrites=true&w=majority')

tpr = Blueprint('tpr', __name__)

@tpr.route('/tpr', methods=['GET'])
def update_tpr():
    client = MongoClient('mongodb+srv://pierre:ztxiGZypi6BGDMSY@atlascluster.sbpp5xm.mongodb.net/?retryWrites=true&w=majority')
    db = client['test']
    collection = db['test2_open']

    #data = list(collection.find())
    data = request.json

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

    client.close()

    return jsonify({'message': 'TPR updated successfully'})
