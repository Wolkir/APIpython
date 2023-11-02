from flask import Flask, Blueprint, jsonify, request, current_app
from pymongo import MongoClient, UpdateOne
from datetime import datetime, timedelta
from typing import Dict, List, Any
import json
import numpy as np

maxprofit_minloss = Blueprint('maxprofit_minloss', __name__)

client = MongoClient('mongodb+srv://pierre:ztxiGZypi6BGDMSY@atlascluster.sbpp5xm.mongodb.net/?retryWrites=true&w=majority')
db = client['test']


@maxprofit_minloss.route('/maxprofit_minloss', methods=['GET'])
def find_max_profit_and_min_loss():
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
        collection_temporaire = db[f"utile_{username}_temporaire"]  # valeur sans conséquence pour pouvoir initialiser la variable

        print("tableauFiltreValue : ", tableauFiltreValue)
        print("collection_name : ", collection_name)
        print("username : ", username)
        print("filtreDeBase : ", filtreDeBase)
        print("filtreAnnexe : ", filtreAnnexe)
        print("dateDebut : ", dateDebut)
        print("dateFin : ", dateFin)



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
            print(query)
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
            print(query)

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

        print("documents : ", documents)



        # ================= SUPPRESSION DES NOMBRE A VIRGULES ================= #



        for data in documents:
            for key, value in data.items():
                if isinstance(value, float):
                    data[key] = int(value)




        # ================= CREATION DICTIONNAIRE DES TRADE TRIES ================= #



        donnees_par_psychologie: Dict[str, List[Any]] = {}

        for doc in documents:
            psychologie = doc.get(filtreAnnexe)
            if psychologie is not None:
                if psychologie not in donnees_par_psychologie:
                    donnees_par_psychologie[psychologie] = []
                donnees_par_psychologie[psychologie].append(doc)



        # ================= CALCUL DE SLR ================= #
        


        resultats_par_psychologie = {}
        typeEnregistrement = ""
        resultats_modifies = {}

        max_profit_value = float('-inf')
        min_loss_value = float('inf')
        max_equity = None
        all_profits = []

        for psychologie, donnees in donnees_par_psychologie.items():
            if psychologie not in resultats_par_psychologie:
                for doc in donnees:
                    profit = doc['profit']
                    all_profits.append(profit)

                    if profit > max_profit_value:
                        max_profit_value = profit

                    if profit < min_loss_value:
                        min_loss_value = profit

                    equity = doc.get('Equity')
                    if equity is not None and equity < 0:
                        if max_equity is None or equity < max_equity:
                            max_equity = equity

                    all_profits_arr = np.array(all_profits)

                    sharpe_ratio = np.mean(all_profits_arr) / np.std(all_profits_arr) if np.std(all_profits_arr) > 0 else 0                  

                    resultats_par_psychologie[psychologie] = {
                        f'{filtreDeBase}_sharpe': sharpe_ratio,
                        f'{filtreDeBase}_maxProfit': max_profit_value,
                        f'{filtreDeBase}_maxLoss': min_loss_value,
                        f'{filtreDeBase}_DDmax': max_equity,
                    }

                print(resultats_par_psychologie)
        """
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
        """




        # ================= FINITION ================= #
        


        """
        for item in tableauFiltreValue:
            for key, value in item.items():
                if key == filtreAnnexe:
                    enregistrement[0][f'{filtreDeBase}_{filtreAnnexe}_colere'] = winrate_value
        """
        new_dict = {}

        for key, value in resultats_par_psychologie.items():
            if not isinstance(key, str):
                key = str(key)
            new_dict[key] = value
            print(f"Clé: {key}, Type de la clé: {type(key)}")

        print(new_dict)



        # ================= ENREGISTREMENT DES WINRATE ================= #



        result = collection_temporaire.update_one({'typeEnregistrement': typeEnregistrement}, {'$set': new_dict}, upsert=True)

        if result:
            print("Données enregistrées avec succès dans la collection temporaire.")
        else:
            print("Erreur lors de l'enregistrement des données dans la collection temporaire.")

        return jsonify(new_dict), 200
    except Exception as e:
        current_app.logger.error(f"Error occurred: {e}")
        return jsonify({"error": str(e)}), 500
