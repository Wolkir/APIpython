from flask import Blueprint, jsonify, request, current_app
from flask_pymongo import PyMongo
import jwt
from bson import ObjectId


correctionTrade = Blueprint('correctionTrade', __name__)

def convert_to_json_serializable(data):
    for key, value in data.items():
        if isinstance(value, bytes):
            data[key] = str(value)
        elif isinstance(value, ObjectId):
            data[key] = str(value)
        elif isinstance(value, dict):
            data[key] = convert_to_json_serializable(value)
    return data

def set_correctionTrade(app):

    @correctionTrade.route('/correctionTrade', methods=['POST', 'OPTIONS'])
    def update_correctionTrade():
        if request.method == 'OPTIONS':
            return jsonify({}), 200
        try:
            mongo = PyMongo(current_app)

            data = request.get_json()
            collection = data.get('collection', None)
            id = data.get('id', None)
            ticketNumber = data.get('ticketNumber', None)
            identifier = data.get('identifier', None)
            magicNumber = data.get('magicNumber', None)
            dateAndTimeOpening = data.get('dateAndTimeOpening', None)
            typeOfTransaction = data.get('typeOfTransaction', None)
            orderType = data.get('orderType', None)
            volume = data.get('volume', None)
            symbol = data.get('symbol', None)
            priceOpening = data.get('priceOpening', None)
            stopLoss = data.get('stopLoss', None)
            takeProfit = data.get('takeProfit', None)
            dateAndTimeClosure = data.get('dateAndTimeClosure', None)
            priceClosure = data.get('priceClosure', None)
            swap = data.get('swap', None)
            profit = data.get('profit', None)
            commission = data.get('commision', None)
            closurePosition = data.get('closurePosition', None)
            balance = data.get('balance', None)

            update_data = {
                '$set': {
                    'ticketNumber': ticketNumber,
                    'identifier': identifier,
                    'magicNumber': magicNumber,
                    'dateAndTimeOpening': dateAndTimeOpening,
                    'typeOfTransaction': typeOfTransaction,
                    'orderType': orderType,
                    'volume': volume,
                    'symbol': symbol,
                    'priceOpening': priceOpening,
                    'stopLoss': stopLoss,
                    'takeProfit': takeProfit,
                    'dateAndTimeClosure': dateAndTimeClosure,
                    'priceClosure': priceClosure,
                    'swap': swap,
                    'profit': profit,
                    'commission': commission,
                    'closurePosition': closurePosition,
                    'balance': balance,
                }
            }

            result = mongo.db[collection].update_one({'_id': ObjectId(id)}, update_data)

            if result.modified_count > 0:
                return jsonify({"message": "Trade details updated successfully."}), 200
            else:
                return jsonify({"message": "No trade was updated."}), 200

        except Exception as e:
            current_app.logger.error(f"Error occurred: {e}")
            return jsonify({"error": str(e)}), 500

    return correctionTrade
