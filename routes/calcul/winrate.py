from flask import Flask, Blueprint, jsonify, request, current_app
from pymongo import MongoClient, UpdateOne
from datetime import datetime, timedelta
from typing import Dict, List, Any
import json
from bson import json_util

winrate = Blueprint('winrate', __name__)

client = MongoClient('mongodb+srv://pierre:ztxiGZypi6BGDMSY@atlascluster.sbpp5xm.mongodb.net/?retryWrites=true&w=majority')
db = client['test']

@winrate.route('/winrate', methods=['GET'])
def calculate_winrate():
    try:



        # ================= RECUPERATION DES ARGUMENTS DE LA REQUETE ================= #



        tableauFiltreValue = []
        dateDebut = ""
        dateFin = ""
        collection_name = ""
        username = ""
        filtreDeBase = ""
        filtreAnnexe = ""
        collection_unitaire = None

        dateDebut = request.args.get('dateDebut', None)
        dateFin = request.args.get('dateFin', None)
        collection_name = request.args.get('collection', None)
        username = request.args.get('username', None)
        filtreDeBase = request.args.get('filtreDeBase', None)
        tableauFiltreValue = request.args.get('tableauFiltreValue', None)
        if tableauFiltreValue is not None:
            tableauFiltreValue = json.loads(tableauFiltreValue)
        else:
            tableauFiltreValue = {}
        filtreAnnexe = list(tableauFiltreValue[0].keys())[0]

        tableauFiltreValue_param = request.args.get('tableauFiltreValue')
        if tableauFiltreValue_param:
            try:
                tableauFiltreValue = json.loads(tableauFiltreValue_param)
            except json.JSONDecodeError:
                print("Erreur lors de la conversion de tableauFiltreValue en JSON.")


        collection = db[collection_name]
        collection_temporaire = db[f"utile_{username}_temporaire"] # valeur sans conséquence pour pouvoir initialiser la variable



        # ================= DATE ================== #

        

        dateDebutFormatee = None
        dateFinFormatee = None
        date_format = '%Y-%m-%dT%H:%M:%S.%fZ'
        if dateDebut is not None and dateFin is not None:
            dateDebutFormatee = datetime.strptime(dateDebut, date_format)
            dateFinFormatee = datetime.strptime(dateFin, date_format)

            print("dateDebutFormatee : ", dateDebutFormatee)
            print("dateFinFormatee : ", dateFinFormatee)

            dateDebutFormatee_str = dateDebutFormatee.strftime('%Y-%m-%d %H:%M:%S')
            dateFinFormatee_str = dateFinFormatee.strftime('%Y-%m-%d %H:%M:%S')

            print("dateDebutFormatee_str : ", dateDebutFormatee_str)
            print("dateFinFormatee_str : ", dateFinFormatee_str)

    

        # ================= CREATION QUERY / TABLEAU ENREGISTREMENT ================= #



        documents = []
        or_conditions = []
        enregistrement = []
        query = {'$and': []}

        if dateDebutFormatee is not None and dateFinFormatee is not None:
            query['$and'].append({'dateAndTimeOpening': {'$gte': dateDebutFormatee_str, '$lt': dateFinFormatee_str}})
        else:
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




        # ================= SUPPRESSION VARIABLES INUTILES ================= #


        if filtreAnnexe == 'Percent':
            variableRequise = ['Percent', 'session', 'profit', 'identifier']

            for d in documents:
                clés_a_supprimer = [cle for cle in d.keys() if cle not in variableRequise]
                
                for cle in clés_a_supprimer:
                    del d[cle]




        # ================= RECUPERATION ECHELLE PERCENT ================= #


        if filtreAnnexe == 'Percent':
            minPercent = float('inf')
            maxPercent = float('-inf')

            for d in documents:
                for cle, valeur in d.items():
                    if cle in variableRequise:
                        if cle == 'Percent':
                            if valeur < minPercent:
                                minPercent = valeur
                            if valeur > maxPercent:
                                maxPercent = valeur

            differencePercent = maxPercent - minPercent

            divisionPercent = differencePercent / 5



        # ================= TRIE ================= #

        

        if filtreAnnexe == 'Percent':
            compte1 = 0.0
            compte2 = round(divisionPercent, 1)
            nouveau_tableau = {}

            while compte2 <= differencePercent:
                tranche = None

                tranche = f'{int(compte1) if compte1.is_integer() else compte1:.1f} - {int(compte2) if compte2.is_integer() else compte2:.1f}'

                if tranche not in nouveau_tableau:
                    nouveau_tableau[tranche] = []

                for data in documents:
                    if 'Percent' in data:
                        percent_value = data['Percent']
                        if compte1 <= percent_value < compte2:
                            nouveau_tableau[tranche].append(data)

                compte1 = round(compte1 + divisionPercent, 1)
                compte2 = round(compte2 + divisionPercent, 1)

            print(nouveau_tableau)




        # ================= CREATION DICTIONNAIRE DES TRADE TRIES ================= #



        donnees_par_psychologie: Dict[str, List[Any]] = {}

        for doc in documents:
            psychologie = doc.get(filtreAnnexe)
            if psychologie is not None:
                if psychologie not in donnees_par_psychologie:
                    donnees_par_psychologie[psychologie] = []
                donnees_par_psychologie[psychologie].append(doc)



        # ================= CALCUL DU WINRATE ================= #



        resultats_par_tranche = {}

        if filtreAnnexe == 'Percent':
            winrate_value = 0
            typeEnregistrement = ""

            for tranche, donnees in nouveau_tableau.items():
                tranche_str = str(tranche)  
                if tranche_str not in resultats_par_tranche:

                    # Déclaration de variables
                    positive_profits_count = 0
                    negative_profits_count = 0
                    positive_identifiers = set()
                    negative_identifiers = set()

                    for doc in donnees:
                        # Calcul
                        profit = doc.get('profit')
                        identifier = doc.get('identifier')

                        if profit is not None and identifier is not None:
                            if profit > 0 and identifier not in positive_identifiers:
                                positive_profits_count += 1
                                positive_identifiers.add(identifier)
                            elif profit < 0 and identifier not in negative_identifiers:
                                negative_profits_count += 1
                                negative_identifiers.add(identifier)

                    if positive_profits_count != 0 and negative_profits_count != 0:
                        winrate_value = positive_profits_count / (positive_profits_count + negative_profits_count) * 100

                    resultats_par_tranche[tranche] = {
                        f'{filtreDeBase}_value': winrate_value
                    }
        else:
            resultats_par_psychologie = {}
            winrate_value = 0
            typeEnregistrement = ""
            resultats_modifies = {}

            for psychologie, donnees in donnees_par_psychologie.items():
                if psychologie not in resultats_par_psychologie:

                    # déclaration variable
                    positive_profits_count = 0
                    negative_profits_count = 0
                    positive_identifiers = set()
                    negative_identifiers = set()

                    for doc in donnees:

                        # calcul
                        profit = doc.get('profit')
                        identifier = doc.get('identifier')

                        if profit is not None and identifier is not None:
                            if profit > 0 and identifier not in positive_identifiers:
                                positive_profits_count += 1
                                positive_identifiers.add(identifier)
                            elif profit < 0 and identifier not in negative_identifiers:
                                negative_profits_count += 1
                                negative_identifiers.add(identifier)

                    print("session : ", doc.get('session'))
                    print("positive_profits_count : ", positive_profits_count)
                    print("negative_profits_count : ", negative_profits_count)

                    if positive_profits_count != 0 and negative_profits_count != 0:
                        winrate_value = positive_profits_count / (positive_profits_count + negative_profits_count) * 100

                    # assignation de la valeur au tableau
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



        # ================= ENREGISTREMENT DES WINRATE ================= #

        print("succes")



        if filtreAnnexe == 'Percent':
            return jsonify(resultats_par_tranche), 200
        else:
            return json_util.dumps(resultats_modifies), 200
    except Exception as e:
        current_app.logger.error(f"Error occurred: {e}")
        return jsonify({"error": str(e)}), 500
