from flask import Flask, Blueprint, jsonify
from pymongo import MongoClient

BE = Blueprint('BE', __name__)

# Connexion à la base de données MongoDB
client = MongoClient('mongodb+srv://pierre:ztxiGZypi6BGDMSY@atlascluster.sbpp5xm.mongodb.net/?retryWrites=true&w=majority')
db = client['test']

def find_BE(username):
    username = data.get('username')
    collection_name = f"{username}_close"
    collection = db[collection_name]

    resultBE = []
    for order in collection.find({'type': 'Close'}):
        rr = order.get('RR', None)
        if rr is not None and -0.5 < rr < 0.5:
            order['BE'] = True
        else:
            order['BE'] = False
        resultBE.append(order)

    return resultBE

if __name__ == '__main__':
    app = Flask(__name__)
    app.register_blueprint(BE)
    app.run()
