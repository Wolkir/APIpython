from flask import Flask, Blueprint, jsonify, request
from flask_pymongo import PyMongo
from pymongo import MongoClient
import bcrypt

# Connexion à la base de données MongoDB
client = MongoClient("mongodb+srv://pierre:ztxiGZypi6BGDMSY@atlascluster.sbpp5xm.mongodb.net/test?retryWrites=true&w=majority")
db = client["test"]

app = Flask(__name__)

trade_blueprint = Blueprint('trade', __name__)

def compare_passwords(password, hashed_password):
    return bcrypt.checkpw(password.encode('utf-8'), hashed_password)

@trade_blueprint.route('/savetraderequest', methods=['POST'])
def save_trade_request():
    data = request.json
    username = data.get('username')
    password = data.get('password')
    closure_position = data.get('closurePosition')

    try:
        user = db.users.find_one({"username": username})
        if not user or not compare_passwords(password, user['password']):
            return jsonify({"message": "Access denied"}), 401

        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

        collection_name = f"{username}_open" if closure_position == "Open" else f"{username}_close"

        user_collection = db[collection_name]

        if closure_position == "Open":
            # For 'Open' orders, copy the 'volume' to 'volume_remain'
            data['volume_remain'] = data['volume']
        else:
            # For 'Close' orders, deduct the 'volume' from the corresponding 'Open' order's 'volume_remain'
            open_orders = db[f"{username}_open"]
            open_order = open_orders.find_one({"identifier": data.get('identifier')})
            if open_order and open_order['volume_remain'] >= data.get('volume'):
                new_volume_remain = open_order['volume_remain'] - data.get('volume')
                if new_volume_remain == 0:
                    open_orders.delete_one({"identifier": data.get('identifier')})
                else:
                    open_orders.update_one({"identifier": data.get('identifier')}, {"$set": {"volume_remain": new_volume_remain}})
            else:
                return jsonify({"message": "Insufficient volume_remain in 'Open' order"}), 400

        trade_request = {
            "username": username,
            "password": hashed_password,
            "ticketNumber": data.get('ticketNumber'),
            "identifier": data.get('identifier'),
            "magicNumber": data.get('magicNumber'),
            "dateAndTimeOpening": data.get('dateAndTimeOpening'),
            "typeOfTransaction": data.get('typeOfTransaction'),
            "volume": data.get('volume'),
            "symbol": data.get('symbol'),
            "priceOpening": data.get('priceOpening'),
            "stopLoss": data.get('stopLoss'),
            "takeProfit": data.get('takeProfit'),
            "dateAndTimeClosure": data.get('dateAndTimeClosure'),
            "priceClosure": data.get('priceClosure'),
            "swap": data.get('swap'),
            "profit": data.get('profit'),
            "commission": data.get('commission'),
            "closurePosition": closure_position,
            "balance": data.get('balance'),
            "broker": data.get('broker'),
            "annonceEconomique": None,
            "psychologie": None,
            "strategie": None,
        }

        user_collection.insert_one(trade_request)
        return jsonify({"message": "Data saved successfully Python v6"}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 400

# Enregistrement du blueprint dans l'application Flask
app.register_blueprint(trade_blueprint, url_prefix='/api')
