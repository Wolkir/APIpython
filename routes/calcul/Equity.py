from flask import Flask, request, jsonify, Blueprint
from pymongo import MongoClient

app = Flask(__name__)
client = MongoClient("mongodb+srv://pierre:ztxiGZypi6BGDMSY@atlascluster.sbpp5xm.mongodb.net/test?retryWrites=true&w=majority")
db = client["test"]

Equity = Blueprint('Equity', __name__)

@Equity.route('/equity', methods=['GET'])
def calculate_equity(data):
    latest_entry = db.test2_close.find_one({}, sort=[("Equity", DESCENDING)])
    preivous_entry = latest_entry["Equity"] if latest_entry is not None else 2
    #previous_equity = 2
    profit = data['profit']
    equity = profit + 2
    
    return equity




