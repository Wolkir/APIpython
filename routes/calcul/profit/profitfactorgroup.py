from flask import Flask, jsonify,Blueprint, request
from pymongo import MongoClient

app = Flask(__name__)

# Connexion à la base de données MongoDB
client = MongoClient('mongodb+srv://pierre:ztxiGZypi6BGDMSY@atlascluster.sbpp5xm.mongodb.net/?retryWrites=true&w=majority')
db = client['test']
profitfactorgroup = Blueprint('profitfactorgroup', __name__)


@app.route('/profitfactorgroup', methods=['GET'])

def calculate_profit_factor_group(data):
    username = data.get('username')
    collection_name = f"{username}_close"
    collection_unitaire = f"{username}_unitaire"
    collection = db[collection_name]

    # Calcul du profit total et du perte total pour toutes les transactions
    total_profit = 0
    total_loss = 0

    # Calcul du profit total et du perte total pour les transactions de type "Buy" uniquement
    total_profit_buy = 0
    total_loss_buy = 0

    # Calcul du profit total et du perte total pour les transactions de type "Sell" uniquement
    total_profit_sell = 0
    total_loss_sell = 0

    # Parcourir les documents de la collection
    for doc in collection.find():
        profit = doc['profit']
        type_of_transaction = doc['typeOfTransaction']
        
        if profit > 0:
            total_profit += profit
        elif profit < 0:
            total_loss += profit

        # Si la transaction est de type "Buy"
        if type_of_transaction == "Buy":
            if profit > 0:
                total_profit_buy += profit
            elif profit < 0:
                total_loss_buy += profit
        
        # Si la transaction est de type "Sell"
        elif type_of_transaction == "Sell":
            if profit > 0:
                total_profit_sell += profit
            elif profit < 0:
                total_loss_sell += profit

    # Calcul du profit factor pour toutes les transactions
    profit_factor = total_profit / abs(total_loss)

    # Calcul du profit factor pour les transactions de type "Buy" uniquement
    profit_factor_buy = total_profit_buy / abs(total_loss_buy)

    # Calcul du profit factor pour les transactions de type "Sell" uniquement
    profit_factor_sell = total_profit_sell / abs(total_loss_sell)

    # Insérer toutes les valeurs dans la collection "unitaire"
    unitaire_collection = db[collection_unitaire]
    unitaire_collection.update_one(
        {},
        {
            '$set': {
                'profitfactor': profit_factor,
                'profitfactorlong': profit_factor_buy,
                'profitfactorshort': profit_factor_sell,
                'total gain': total_profit,
                'total loss': total_loss,
                'total gain long': total_profit_buy,
                'total loss long': total_loss_buy,
                'total gain short': total_profit_sell,
                'total loss short': total_loss_sell            
                
            }
        },
        upsert=True
    )
