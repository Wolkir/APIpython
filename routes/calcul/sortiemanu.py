from flask import Flask, Blueprint, jsonify, request
from pymongo import MongoClient
from routes.calcul.TPR import calculate_tpr
from routes.calcul.SLR import calculate_slr
from bson import ObjectId

app = Flask(__name__)

# Connection to MongoDB database
client = MongoClient('mongodb+srv://pierre:ztxiGZypi6BGDMSY@atlascluster.sbpp5xm.mongodb.net/?retryWrites=true&w=majority')
db = client['test']

sortiemanu = Blueprint('sortiemanu', __name__)


@app.route('/sortiemanu', methods=['GET'])
def calculate_sortiemanu(data):
    
    username = data.get('username')
    collection_name = f"{username}_close"
    collection = db[collection_name]
    
    closurePosition = data.get('closurePosition')
    
    # Use functions to get TPR and SLR
    TPRMan = calculate_tpr(data)
    SLRMan = calculate_slr(data)

    if closurePosition == 'Close' and not TPRMan and not SLRMan:
        Smanu = True
    else:
        Smanu = False

    return jsonify({'Smanu': Smanu})
