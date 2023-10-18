from flask import Flask, Blueprint, request, jsonify
from pymongo import MongoClient
from datetime import datetime

client = MongoClient('mongodb+srv://pierre:ztxiGZypi6BGDMSY@atlascluster.sbpp5xm.mongodb.net/?retryWrites=true&w=majority')
db = client['test']
collection = db['Note']

enregistrerNote = Blueprint('enregistrerNote', __name__)

@enregistrerNote.route('/enregistrerNote', methods=['POST'])
def enregistrer_note():
    username = request.form.get('username')
    titre_value = request.form.get('titreValue')
    texte_value = request.form.get('texteValue')

    formatted_date = datetime.now().strftime('%d %B %Y')
    date_iso = datetime.now().replace(microsecond=0).isoformat() + "+00:00"
  
    if username and titre_value and texte_value:
        note = {
            'username': username,
            'titreValue': titre_value,
            'texteValue': texte_value,
            'datePrecise': date_iso,
            'date': formatted_date
        }
        collection.insert_one(note)
        return jsonify({"message": "Note enregistrée avec succès!"}), 201
    else:
        return jsonify({"error": "Paramètres manquants"}), 400
