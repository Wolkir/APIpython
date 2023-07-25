from flask import Flask, Blueprint, jsonify
from pymongo import MongoClient
from datetime import datetime

# Connexion à la base de données MongoDB
client = MongoClient('mongodb+srv://pierre:ztxiGZypi6BGDMSY@atlascluster.sbpp5xm.mongodb.net/?retryWrites=true&w=majority')
db = client['test']
collection = db['things']

calculate_duration = Blueprint('calculate_duration', __name__)

@calculate_duration.route('/calculate_duration', methods=['GET'])
def calculate_time_duration():
    try:
        # Récupérer les documents avec les dates de départ et de fin
        documents = collection.find()
        
        # Calculer la durée pour chaque document et mettre à jour la collection
        for doc in documents:
            opening_time = doc['dateAndTimeOpening']
            closure_time = doc['dateAndTimeClosure']
            
            # Calculer la durée
            duration = closure_time - opening_time
            
            # Mettre à jour le document avec la clé 'durée' et sa valeur
            collection.update_one({'_id': doc['_id']}, {'$set': {'durée': str(duration)}})
        
        return jsonify({"message": "La clé 'durée' a été ajoutée à la collection 'things'"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400
