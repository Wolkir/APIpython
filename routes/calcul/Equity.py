from flask import Flask, request, jsonify, Blueprint
from pymongo import MongoClient

app = Flask(__name__)
client = MongoClient("mongodb+srv://pierre:ztxiGZypi6BGDMSY@atlascluster.sbpp5xm.mongodb.net/test?retryWrites=true&w=majority")
db = client["test"]

Equity = Blueprint('Equity', __name__)

@Equity.route('/equity', methods=['GET'])
def calculate_equity(data):
    previous_equity = 2

    profit = data['profit']
    equity = previous_equity + profit
    
    return equity
