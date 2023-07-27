from flask import Flask, Blueprint, jsonify, request
from pymongo import MongoClient
import bcrypt
from datetime import time
from routes.calcul.TPR import calculate_tpr
from routes.calcul.SLR import calculate_slr
from routes.calcul.killzone import calculate_killzone
from routes.calcul.session import determine_session
from routes.calcul.calculate_duration import calculate_time_duration
from routes.calcul.RR import calculate_rr
from routes.calcul.RRT import calculate_rrt
from routes.calcul.Equity import calculate_equity

# Connexion à la base de données MongoDB
client = MongoClient("mongodb+srv://pierre:ztxiGZypi6BGDMSY@atlascluster.sbpp5xm.mongodb.net/test?retryWrites=true&w=majority")
db = client["test"]

app = Flask(__name__)

# Trade Blueprint
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
            volume_remain = data.get('volume')
            if volume_remain < 0.01:
                volume_remain = 0
                user_collection.delete_one({"identifier": data.get('identifier')})
        else:
            # Check if there's a corresponding 'Open' order with the same identifier
            open_orders = db[f"{username}_open"]
            open_order = open_orders.find_one({"identifier": data.get('identifier')})
            if open_order:
                volume_remain = open_order.get('volume_remain', 0) - data.get('volume')
                if volume_remain < 0:
                    volume_remain = 0
                open_orders.update_one({"identifier": data.get('identifier')}, {"$set": {"volume_remain": volume_remain}})
                if volume_remain == 0:
                    open_orders.delete_one({"identifier": data.get('identifier')})
            else:
                return jsonify({"message": "No corresponding 'Open' order found"}), 400

        # Remove 'volume_remain' field for 'Close' orders
        if closure_position == "Close":
            data.pop("volume_remain", None)

            # Calculate SLR only for 'Close' orders
            slr_value = calculate_slr(data)
            data['SLR'] = slr_value['SLR']

            # Calculate TPR only for 'Close' orders
            tpr_value = calculate_tpr(data)
            data['TPR'] = tpr_value['TPR']

            killzone = calculate_killzone(data)
            data['killzone'] = killzone

            session = determine_session(data)
            data['session'] = session

            duration = calculate_time_duration(data)
            data['duration'] = duration['duration']

            rr = calculate_rr(data)
            data['RR'] = rr

            rrt = calculate_rrt(data)
            data['RRT'] = rrt

            last_equity= calculate_equity(data)
            data['Equity'] = last_equity
       

          

        # Round 'volume' and 'volume_remain' to two decimal places
        data['volume'] = round(data.get('volume'), 2)
        volume_remain = round(volume_remain, 2)

        # Calculate killzone only for 'Open' orders
        if closure_position == "Open":
            killzone = calculate_killzone(data)
            data['killzone'] = killzone

            session = determine_session(data)
            data['session'] = session

            rrt = calculate_rrt(data)
            data['RRT'] = rrt
            
        # Insert the data into the collection
        #user_collection.insert_one(data)

        trade_request = {
            "username": username,
            "password": hashed_password,
            "ticketNumber": data.get('ticketNumber'),
            "identifier": data.get('identifier'),
            "magicNumber": data.get('magicNumber'),
            "dateAndTimeOpening": data.get('dateAndTimeOpening'),
            "typeOfTransaction": data.get('typeOfTransaction'),
            "typeOrder": data.get('typeOrder'),
            "volume": data.get('volume'),
            "volume_remain": volume_remain,
            "symbol": data.get('symbole'),
            "priceOpening": data.get('priceOpening'),
            "stopLoss": data.get('stopLoss'),
            "takeProfit": data.get('takeProfit'),
            "dateAndTimeClosure": data.get('dateAndTimeClosure'),
            "priceClosure": data.get('priceClosure'),
            "swap": data.get('swap'),
            "profit": data.get('profit'),
            "commission": data.get('commision'),
            "closurePosition": data.get('closurePosition'),
            "balance": data.get('balance'),
            "broker": data.get('broker'),
            "annonceEconomique": None,
            "psychologie": None,
            "strategie": None,
            "position": None,
            "typeOrdre": None,
            "violeStrategie": None,
            "sortie": None,
            "killzone": data.get("killzone"),
            "session": data.get("session"),
            "duration": data.get('duration'),
            "TPR": data.get('TPR'),
            "SLR": data.get('SLR'),
            "RR": data.get('RR'),
            "RRT": data.get('RRT'),
            "Equity": data.get('Equity')
        }
        #combined_data = [trade_request, data]
        # Insertion des données dans la collection
        user_collection.insert_one(trade_request)

        return jsonify({"message": "Data saved successfully with TPR and SLR kill"}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 400

# Enregistrement du blueprint "trade" dans l'application Flask
app.register_blueprint(trade_blueprint, url_prefix='/api')


if __name__ == '__main__':
    app.run()
