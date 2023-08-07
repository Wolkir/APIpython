from flask import Flask, Blueprint, jsonify, request
from pymongo import MongoClient

app = Flask(__name__)

# Connexion à la base de données MongoDB
client = MongoClient('mongodb+srv://pierre:ztxiGZypi6BGDMSY@atlascluster.sbpp5xm.mongodb.net/?retryWrites=true&w=majority')
db = client['test']

# Blueprint pour /sortiemanu
sortiemanu = Blueprint('sortiemanu', __name__)

@sortiemanu.route('/sortiemanu', methods=['GET'])
def calculate_sortiemanu(data):
    data = request.json

    username = data.get('username')
    collection_name = f"{username}_close"
    collection = db[collection_name]
  
    closurePosition = data.get('closurePosition')
    TPR_value = data.get('TPR')
    SLR_value = data.get('SLR')
    Smanu_value=None
    # Check if closurePosition is "Close", TPR is "False", and SLR is "False"
    if closurePosition == 'Close' and TPR_value == False and SLR_value == False:
        Smanu_value = True
    else:
        Smanu_value = False
    
    # Return the result in JSON format
    return Smanu_value


