from flask import Flask, Blueprint, jsonify, request
from pymongo import MongoClient

winrate = Blueprint('winrate', __name__)

# Connexion à la base de données MongoDB
client = MongoClient('mongodb+srv://pierre:ztxiGZypi6BGDMSY@atlascluster.sbpp5xm.mongodb.net/?retryWrites=true&w=majority')
db = client['test']

@winrate.route('/winrate', methods=['GET'])
def calculate_winrate():
    try:
        collection = request.args.get('collection', None)
        username = request.args.get('username', None)
        filtreDeBase = request.args.get('filtreDeBase', None)
        tableauFiltreValue_json = request.args.get('tableauFiltreValue')
        tableauFiltreValue = json.loads(tableauFiltreValue_json)
        
        collection_unitaire = f"{username}_unitaire"
        collection = db[collection_name]

        print(collection_name)
        print(username)
        print(filtreDeBase)
        print(tableauFiltreValue)
        print(collection_unitaire)
        print(collection)
      
        documents = list(collection.find())
        
        print(documents)

        query = {}

        for item in tableauFiltreValue:
            condition = {}
            for key, value in item.items():
                condition[key] = {'$ne': value}
            or_conditions.append(condition)
    
        query = {'$and': or_conditions}
        
        positive_profits_count = 0
        negative_profits_count = 0
        
        positive_identifiers = set()
        negative_identifiers = set()
        
        for doc in documents:
            profit = doc['profit']
            identifier = doc['identifier']
            print(doc)
            
            if profit > 0 and identifier not in positive_identifiers:
                positive_profits_count += 1
                positive_identifiers.add(identifier)
            elif profit < 0 and identifier not in negative_identifiers:
                negative_profits_count += 1
                negative_identifiers.add(identifier)
    

        winrate_value = positive_profits_count / (positive_profits_count + negative_profits_count) * 100

        print(positive_profits_count)
        print(negative_profits_count)
        print(winrate_value)
   
        # Insérer le winrate_value dans la collection "unitaire"
        unitaire_collection = db[collection_unitaire]
        unitaire_collection.update_one({}, {'$set': {'winratereal': (winrate_value)}}, upsert=True)

        return jsonify({
            "message": "Données traitées avec succès",
            "query": query
        })
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    except:
        return jsonify({"error": "La demande ne contient pas de données JSON valide"}), 400

