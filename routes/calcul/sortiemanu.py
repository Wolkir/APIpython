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

    username = data.get('username')
    collection_name = f"{username}_close"
    collection = db[collection_name]
  
    closurePosition = data.get('closurePosition')
    TPR = data.get('TPR')
    SLR = data.get('SLR')

    # Check if closurePosition is "Close", TPR is "False", and SLR is "False"
    if closurePosition == 'Close' and TPR == 'False' and SLR == 'False':
        Smanu = 'True'
    else:
        Smanu = 'False'
    
    # Return the result
    return Smanu

       
