from flask import Flask, Blueprint, jsonify
from pymongo import MongoClient

app = Flask(__name__)
profitfactor = Blueprint('profitfactor', __name__)

# Connexion à la base de données MongoDB
client = MongoClient('mongodb+srv://pierre:ztxiGZypi6BGDMSY@atlascluster.sbpp5xm.mongodb.net/?retryWrites=true&w=majority')
db = client['test']
collection = db['things']

@profitfactor.route('/profitfactor', methods=['GET'])
def calculate_profit_factor():
    # Calcul du profit total et du perte total
    total_profit = 0
    total_loss = 0

    # Parcourir les documents de la collection
    for doc in collection.find():
        profit = doc['profit']
        if profit > 0:
            total_profit += profit
        elif profit < 0:
            total_loss += profit
    print(f"Total du profit : {total_profit}")
    print(f"Total de la perte : {total_loss}")
    # Calcul du profit factor
    profit_factor = total_profit / abs(total_loss)

    # Insérer le winrate_value dans la collection "unitaire"
    unitaire_collection = db['unitaire']
    unitaire_collection.insert_one({"profitfactor": profit_factor})
    unitaire_collection.insert_one({"total_profit": total_profit})
    unitaire_collection.insert_one({"total_loss": total_loss})

    return jsonify({"profit_factor": str(profit_factor)})

def main():
    app.register_blueprint(profitfactor)

    if __name__ == '__main__':
        with app.app_context():
            app.run()

if __name__ == '__main__':
    main()
