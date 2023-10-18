from flask import Blueprint, jsonify, request
from pymongo import MongoClient

client = MongoClient('mongodb+srv://pierre:ztxiGZypi6BGDMSY@atlascluster.sbpp5xm.mongodb.net/?retryWrites=true&w=majority')
db = client['test']
collection = db['Note']

recuperationNote = Blueprint('recuperationNote', __name__)

@recuperationNote.route('/recuperationNote', methods=['GET'])
def get_notes():
    username = request.args.get('username')
    argRechercheDonnee = request.args.get('rechercheNoteValue', None)
    
    query = {
        '$and': [
            {'username': username},
        ]
    }

    if argRechercheDonnee is not None and argRechercheDonnee != "":
        regex_pattern = f".*{argRechercheDonnee}.*"
        query['$and'].append({'titreValue': {'$regex': regex_pattern}})
    if username:
        notes = list(collection.find(query))
        
        serialized_notes = []
        for note in notes:
            serialized_note = {
                'id': str(note['_id']),
                'username': note['username'],
                'titreValue': note['titreValue'],
                'texteValue': note['texteValue'],
                'datePrecise': note['datePrecise'],
                'date': note['date']
            }
            serialized_notes.append(serialized_note)

        return jsonify(serialized_notes)
    else:
        return jsonify({'error': 'Paramètre "username" manquant'})
