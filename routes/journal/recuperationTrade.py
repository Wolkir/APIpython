def setup_things_routes(app):
    @things_blueprint.route('/recuperationTrade', methods=['GET'])
    def get_all_things():
        try:
            mongo = PyMongo(current_app)
            db = mongo.db

            argUsername = request.args.get('username', None)
            argTypeTrade = request.args.get('typeTrade', None)
            argCollection = request.args.get('collection', None)

            # Vérifier si l'argument collection est "tout"
            if argCollection == "tout":
                # Si c'est le cas, renvoyer toutes les collections pour l'utilisateur spécifié
                data = [name for name in db.list_collection_names() if argUsername in name]
                collections = [name.replace("_" + argUsername, "").replace(argUsername + "_", "").replace(argUsername, "") for name in data]

                # Créer un dictionnaire pour chaque collection avec son nom et son contenu
                result = {}
                for collection_name in collections:
                    collection_data = list(db[argUsername + "_" + collection_name].find())
                    collection_data = [convert_to_json_serializable(item) for item in collection_data]
                    result[collection_name] = collection_data

                return jsonify(result), 200

            else:
                collection = argUsername + "_" + argCollection

            query = {'username': argUsername}

            if argTypeTrade is not None and argTypeTrade == "renseigne":
                query['$or'] = [{'annonceEconomique': {'$ne': None}}, {'psychologie': {'$ne': None}}, {'strategie': {'$ne': None}}]
            elif argTypeTrade is not None and argTypeTrade == "nonrenseigne":
                query['$and'] = [{'annonceEconomique': None}, {'Fatigue': None}, {'psychologie': None}]

            things_collection = mongo.db[collection]
            all_things = list(things_collection.find(query))

            result = [convert_to_json_serializable(thing) for thing in all_things]
            return jsonify(result), 200

        except Exception as e:
            return jsonify({"error": str(e)}), 500

    return things_blueprint

