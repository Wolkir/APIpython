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
    
# Use functions to get TPR and SLR


@app.route('/sortiemanu', methods=['GET'])
def calculate_sortiemanu(data):
  
    username = data.get('username')
    collection_name = f"{username}_close"
    collection = db[collection_name]

    closurePosition = data.get('closurePosition')
    orderType = data.get('orderType')
    price_closure = data.get('priceClosure')
    take_profit = data.get('takeProfit')
    stop_loss = data.get('stopLoss')
    profit = data.get('profit')
    
    if orderType == "BUY" and price_closure >= take_profit and take_profit>0:
        tprman = True
    elif orderType == "SELL" and price_closure <= take_profit and take_profit>0 :
        tprman = True
    else:
        tprman = False


  

    if orderType == "BUY" and price_closure <= stop_loss and profit < 0:
        slrman = True
    elif orderType == "SELL" and price_closure >= stop_loss and profit < 0:
        slrman = True
    else:
        slrman = False

  
    if closurePosition == 'Close' and tprman == False and  slrman == False:
        smanu = True
    else:
        smanu = False

