from flask import Flask, Blueprint, jsonify, request
from pymongo import MongoClient

app = Flask(__name__)


# Connexion à la base de données MongoDB
client = MongoClient('mongodb+srv://pierre:ztxiGZypi6BGDMSY@atlascluster.sbpp5xm.mongodb.net/?retryWrites=true&w=majority')
db = client['test']

# Blueprint pour /sortiemanu
sortiemanu = Blueprint('sortiemanu', __name__)

@sortiemanu.route('/sortiemanu', methods=['POST'])
def calculate_sortiemanu(data):
        data = request.json
        username = data.get('username')
        collection = f"{username}_close"
        collection = db[collection_name]
      
    try:
        
        closurePosition = data.get('closurePosition')
        TPR = data.get('TPR')
        SLR = data.get('SLR')

        # Check if closurePosition is "Close", TPR is "False", and SLR is "False"
        if closurePosition == 'Close' and TPR == 'False' and SLR == 'False':
            data['Sortiemanu'] = 'True'

       
