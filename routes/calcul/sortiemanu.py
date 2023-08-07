from flask import Flask, Blueprint, jsonify, request
from pymongo import MongoClient
from tpr import calculate_tpr
from slr import calculate_slr
app = Flask(__name__)

# Connexion à la base de données MongoDB
client = MongoClient('mongodb+srv://pierre:ztxiGZypi6BGDMSY@atlascluster.sbpp5xm.mongodb.net/?retryWrites=true&w=majority')
db = client['test']

# Blueprint pour /sortiemanu
sortiemanu = Blueprint('sortiemanu', __name__)

@sortiemanu.route('/sortiemanu', methods=['GET'])

def calculate_sortiemanu(data):
    username = data.get('username')
    collection_name = f"{username}_close"
    collection = db[collection_name]
    
    closurePosition = data.get('closurePosition')
    
    # Utilisation des fonctions pour obtenir TPR et SLR
    TPR = calculate_tpr(data)
    SLR = calculate_slr(data)

    if closurePosition == 'Close' and not TPR and not SLR:
        Smanu = True
    else:
        Smanu = False

    return jsonify({'Smanu': Smanu})


