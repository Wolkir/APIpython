from flask import Flask, Blueprint, jsonify, request
from typing import Dict, List, Any
from pymongo import MongoClient, UpdateOne

winrate = Blueprint('winrate', __name__)

client = MongoClient('mongodb+srv://pierre:ztxiGZypi6BGDMSY@atlascluster.sbpp5xm.mongodb.net/?retryWrites=true&w=majority')
db = client['test']

@winrate.route('/winrate', methods=['GET'])
def calculate_winrate():
    try:



        # ================= RECUPERATION DES ARGUMENTS DE LA REQUETE ================= #



        data = request.get_json()

        tableauFiltreValue = []
        collection_name = ""
        username = ""
        filtreDeBase = ""
        filtreAnnexe = ""
        premier_element = ""
        
        if isinstance(data, list):
            for item in data:
                collection_name = item.get('collection', None)
                username = item.get('username', None)
                filtreDeBase = item.get('filtreDeBase', None)
                tableauFiltreValue = item.get('tableauFiltreValue', None)
                if isinstance(tableauFiltreValue, list) and len(tableauFiltreValue) > 0:
                    premier_element = tableauFiltreValue[0]
                    filtreAnnexe = list(premier_element.keys())[0]
                    
                #print("argument annexe : ", filtreAnnexe)

                temporaire = f"utile_{username}_temporaire"

                collection_unitaire = f"utile_{username}_unitaire"
                collection_temporaire = db[temporaire]
                collection = db[collection_name]



        # ================= OPTIONS TOUS COLLECTION ================= #

        documents = []

        # ================= CREATION QUERY / TABLEAU ENREGISTREMENT ================= #



        or_conditions = []
        enregistrement = []

        for item in tableauFiltreValue:
            condition = {}
            for key, value in item.items():
                if value is not None:
                    condition[key] = {'$ne': None}
                    ligne = {f"{filtreDeBase}_{key}_{value}": None}
                    enregistrement.append(ligne)
            or_conditions.append(condition)

        query = {'$and': or_conditions}

        if collection_name == "tous":
            exception = "utile"
            toutLesNoms = [name for name in db.list_collection_names() if username in name and exception not in name.split('_')]
            toutes_les_donnees = []
            for collection_name in toutLesNoms:
                collection = db[collection_name]
                data = list(collection.find({}))
                toutes_les_donnees.extend(data)
            documents = toutes_les_donnees
            #print('documents', len(documents))
        else:
            documents = list(collection.find(query))



        # ================= SUPPRESSION DES NOMBRE A VIRGULES ================= #



        for data in documents:
            for key, value in data.items():
                if isinstance(value, float):
                    data[key] = int(value)

        print("documents entier : ", documents)




        # ================= CREATION DICTIONNAIRE DES TRADE TRIES ================= #



        donnees_par_psychologie: Dict[str, List[Any]] = {}

        for doc in documents:
            psychologie = doc.get(filtreAnnexe)
            if psychologie is not None:
                if psychologie not in donnees_par_psychologie:
                    donnees_par_psychologie[psychologie] = []
                donnees_par_psychologie[psychologie].append(doc)



        # ================= CALCUL DU WINRATE ================= #



        """
        positive_profits_count = 0
        negative_profits_count = 0
        
        positive_identifiers = set()
        negative_identifiers = set()
        
        for doc in documents:
            profit = doc['profit']
            identifier = doc['identifier']
            
            if profit > 0 and identifier not in positive_identifiers:
                positive_profits_count += 1
                positive_identifiers.add(identifier)
            elif profit < 0 and identifier not in negative_identifiers:
                negative_profits_count += 1
                negative_identifiers.add(identifier)
    
        winrate_value = positive_profits_count / (positive_profits_count + negative_profits_count) * 100
        """
        resultats_par_psychologie = {}
        winrate_value = 0
        typeEnregistrement = ""
        resultats_modifies = {}

        for psychologie, donnees in donnees_par_psychologie.items():
            if psychologie not in resultats_par_psychologie:
                positive_profits_count = 0
                negative_profits_count = 0
                positive_identifiers = set()
                negative_identifiers = set()

                for doc in donnees:
                    profit = doc.get('profit')
                    identifier = doc.get('identifier')

                    if profit is not None and identifier is not None:
                        if profit > 0 and identifier not in positive_identifiers:
                            positive_profits_count += 1
                            positive_identifiers.add(identifier)
                        elif profit < 0 and identifier not in negative_identifiers:
                            negative_profits_count += 1
                            negative_identifiers.add(identifier)

                winrate_value = positive_profits_count / (positive_profits_count + negative_profits_count) * 100

                resultats_par_psychologie[psychologie] = {
                    f'{filtreDeBase}_value': winrate_value
                }

            resultats_sans_doublons = {}

            for psychologie, resultats in resultats_par_psychologie.items():
                if psychologie not in resultats_sans_doublons:
                    resultats_sans_doublons[psychologie] = resultats

            for psychologie, resultats in resultats_sans_doublons.items():
                nouvelle_cle = f'{psychologie}'
                valeur_winrate = resultats[f'{filtreDeBase}_value']
                
                resultats_modifies[nouvelle_cle] = valeur_winrate

            typeEnregistrement = f"{filtreDeBase}_{filtreAnnexe}"

            resultats_modifies["typeEnregistrement"] = typeEnregistrement



        # ================= FINITION ================= #


        
        for item in tableauFiltreValue:
            for key, value in item.items():
                if key == filtreAnnexe:
                    enregistrement[0][f'{filtreDeBase}_{filtreAnnexe}_colere'] = winrate_value
   
        unitaire_collection = db[collection_unitaire]
        unitaire_collection.update_one({}, {'$set': {'winratereal': (winrate_value)}}, upsert=True)



        # ================= ENREGISTREMENT DES WINRATE ================= #



        result = collection_temporaire.update_one({'typeEnregistrement': typeEnregistrement}, {'$set': resultats_modifies}, upsert=True)

        if result:
            print("Données enregistrées avec succès dans la collection temporaire.")
        else:
            print("Erreur lors de l'enregistrement des données dans la collection temporaire.")

        return jsonify({"message": f"{filtreDeBase} calculé avec succès", "resultats_modifies": resultats_modifies})
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    except:
        return jsonify({"error": "La demande ne contient pas de données JSON valide"}), 400
