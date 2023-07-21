@trade_blueprint.route('/savetraderequest', methods=['POST'])
def save_trade_request():
    data = request.json
    username = data.get('username')
    password = data.get('password')
    closure_position = data.get('closurePosition')

    try:
        # Vérifier l'authentification de l'utilisateur
        user = db.users.find_one({"username": username})
        if not user or not compare_passwords(password, user['password']):
            return jsonify({"message": "Access denied"}), 401

        # Hacher le mot de passe
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

        # Récupérer la collection correspondant au nom d'utilisateur et closurePosition
        if closure_position == "Open":
            collection_name = f"{username}_open"
            user_collection = db[collection_name]

            # Vérifier si un ordre ouvert avec cet identifiant existe déjà
            existing_open_order = user_collection.find_one({"identifier": data.get('identifier'), "closurePosition": "Open"})

            if existing_open_order:
                # Mettre à jour le volume de l'ordre ouvert avec le nouveau volume
                existing_open_order['volume'] = data.get('volume')
                user_collection.replace_one({"_id": existing_open_order["_id"]}, existing_open_order)
            else:
                # Créer une nouvelle instance de TradeRequest pour l'ordre ouvert
                trade_request = {
                    "username": username,
                    "password": hashed_password,
                    "ticketNumber": data.get('ticketNumber'),
                    "identifier": data.get('identifier'),
                    "dateAndTimeOpening": data.get('dateAndTimeOpening'),
                    "typeOfTransaction": data.get('typeOfTransaction'),
                    "volume": data.get('volume'),
                    "symbol": data.get('symbole'),
                    "priceOpening": data.get('priceOpening'),
                    "stopLoss": data.get('stopLoss'),
                    "takeProfit": data.get('takeProfit'),
                    "closurePosition": closure_position
                }

                # Enregistrer l'objet dans la collection de l'utilisateur et closurePosition
                user_collection.insert_one(trade_request)
        else:
            # Si l'ordre est une demande de fermeture, nous devons vérifier s'il correspond à un ordre ouvert existant
            collection_name_open = f"{username}_open"
            collection_name_close = f"{username}_close"
            user_collection_open = db[collection_name_open]
            user_collection_close = db[collection_name_close]

            existing_open_order = user_collection_open.find_one({"identifier": data.get('identifier'), "closurePosition": "Open"})

            if existing_open_order:
                # Mettre à jour le volume fermé pour l'ordre ouvert
                existing_open_order['volume_closed'] = existing_open_order.get('volume_closed', 0) + data.get('volume')

                if existing_open_order['volume_closed'] >= existing_open_order['volume']:
                    # L'ordre ouvert est entièrement fermé, donc nous l'enregistrons dans la collection des ordres fermés
                    user_collection_close.insert_one(existing_open_order)

                    # Supprimer l'ordre ouvert de la collection des ordres ouverts
                    user_collection_open.delete_one({"_id": existing_open_order["_id"]})
                else:
                    # Mettre à jour l'ordre ouvert avec le nouveau volume fermé
                    user_collection_open.replace_one({"_id": existing_open_order["_id"]}, existing_open_order)
            else:
                # Si l'ordre ouvert n'existe pas, nous ne pouvons pas fermer cet ordre
                return jsonify({"message": "Open order not found"}), 404

        return jsonify({"message": "Data saved successfully"}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 400
