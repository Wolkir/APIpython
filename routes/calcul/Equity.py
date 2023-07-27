from flask import Flask, request, jsonify, Blueprint
from pymongo import MongoClient, DESCENDING

app = Flask(__name__)
client = MongoClient("mongodb+srv://pierre:ztxiGZypi6BGDMSY@atlascluster.sbpp5xm.mongodb.net/test?retryWrites=true&w=majority")
db = client["test"]

Equity = Blueprint('Equity', __name__)

@Equity.route('/equity', methods=['GET'])
def calculate_equity(data):
    latest_entry = db.test2_close.find_one({}, sort=[("Equity", DESCENDING)])
    previous_entry = latest_entry.get("Equity", 2)
    profit = data['profit']
    equity = profit + previous_entry
    
    return str(equity)




