from flask import Flask, Blueprint, jsonify, request
from flask import Blueprint, request, jsonify

daytotal = Blueprint('daytotal', __name__)

@daytotal.route('/daytotal', methods=['POST'])  # POST pour la sécurité des données de l'utilisateur
def calculate_daycount(data):
    data = request.json
    username = data.get('username')
    
    if not username:
        return jsonify({"error": "Username is required!"}), 400

    collection_name = f"{username}_close"
    collection = db[collection_name]
    collection_unit = f"{username}_unitaire"
    unitaire_collection = db[collection_unit]
    

    # Supposition qu'il y a un champ 'date' dans chaque document contenant la date
    distinct_dates = collection.aggregate([
        {
            "$group": {
                "_id": "$dateandTimeOpening"
            }
        },
        {
            "$count": "distinctDateCount"
        }
    ])

    result = list(distinct_dates)
    if result:
        distinct_count = result[0]['distinctDateCount']
        unitaire_collection.update_one({}, {"$set": {"daytotal": distinct_count}}, upsert=True)
        return jsonify({"distinctDateCount": distinct_count})
   
    return jsonify({"error": "No distinct dates found"}), 400
