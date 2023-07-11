from flask import Flask, Blueprint, jsonify
from pymongo import MongoClient

app = Flask(__name__)
maxsuccessivegains = Blueprint('maxsuccessivegains', __name__)
from flask import Flask, Blueprint, jsonify
from pymongo import MongoClient

app = Flask(__name__)
max_successive_gains = Blueprint('max_successive_gains', __name__)

# Connexion à la base de données MongoDB
client = MongoClient('mongodb+srv://pierre:ztxiGZypi6BGDMSY@atlascluster.sbpp5xm.mongodb.net/?retryWrites=true&w=majority')
db = client['test']
collection = db['things']

@max_successive_gains.route('/max_successive_gains', methods=['GET'])
def find_max_successive_gains():
    # Initialisation des variables
    max_successive_gains_count = 0
    current_successive_gains_count = 0
    previous_ticket_number = None

    # Parcourir les documents de la collection
    for doc in collection.find().sort("ticketNumber"):
        profit = doc['profit']
        ticket_number = doc['ticketNumber']

        if profit > 0:
            if ticket_number != previous_ticket_number:
                current_successive_gains_count = 1
            else:
                current_successive_gains_count += 1

            if current_successive_gains_count > max_successive_gains_count:
                max_successive_gains_count = current_successive_gains_count

        previous_ticket_number = ticket_number

    return jsonify({"max_successive_gains": max_successive_gains_count})

app.register_blueprint(max_successive_gains)

if __name__ == '__main__':
    app.run()