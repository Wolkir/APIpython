from flask import Flask, Blueprint, request
from pymongo import MongoClient
from datetime import timedelta

app = Flask(__name__)
totaltrade = Blueprint('totaltrade', __name__)

# Connexion à la base de données MongoDB
client = MongoClient('mongodb+srv://pierre:ztxiGZypi6BGDMSY@atlascluster.sbpp5xm.mongodb.net/?retryWrites=true&w=majority')
db = client['test']

@totaltrade.route('/totaltrade', methods=['POST'])
def calculate_totaltrade():
    data = request.get_json()
    username = data.get('username')
    collection_name = f"{username}_close"
    collection = db[collection_name]

    last_trade = collection.find().sort('date', pymongo.DESCENDING).limit(1).to_list(length=1)

    if len(last_trade) == 0:  # if the collection is empty
        totaltrade = 1
    else:
        totaltrade = last_trade[0]['totaltrade'] + 1

    new_trade = data.get('trade')  # get the new trade from the request data
    new_trade['totaltrade'] = totaltrade  # set the totaltrade field for the new trade

    collection.insert_one(new_trade)  # insert the new trade into the collection

    return str(totaltrade), 201  # return the totaltrade value as a string
