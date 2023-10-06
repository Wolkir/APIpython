from pymongo import MongoClient

client = MongoClient('mongodb+srv://pierre:ztxiGZypi6BGDMSY@atlascluster.sbpp5xm.mongodb.net/?retryWrites=true&w=majority')
db = client['test']

def winrateGroup(data, collection_unitaire):
 

    positive_profits_count = 0
    negative_profits_count = 0
    positivelong_profits_count = 0
    negativelong_profits_count = 0
    positiveshort_profits_count = 0
    negativeshort_profits_count = 0

    positive_identifiers = set()
    negative_identifiers = set()
    positivelong_identifiers = set()
    negativelong_identifiers = set()
    positiveshort_identifiers = set()
    negativeshort_identifiers = set()

    for doc in data:
        profit = doc['profit']
        identifier = doc['identifier']
        
        is_buy_order = doc['orderType'] == "BUY"
        is_sell_order = doc['orderType'] == "SELL"

        if profit > 0 and identifier not in positive_identifiers:
            positive_profits_count += 1
            positive_identifiers.add(identifier)

            if is_buy_order and identifier not in positivelong_identifiers:
                positivelong_profits_count += 1
                positivelong_identifiers.add(identifier)
            if is_sell_order and identifier not in positiveshort_identifiers:
                positiveshort_profits_count += 1
                positiveshort_identifiers.add(identifier)

        elif profit < 0 and identifier not in negative_identifiers:
            negative_profits_count += 1
            negative_identifiers.add(identifier)

            if is_buy_order and identifier not in negativelong_identifiers:
                negativelong_profits_count += 1
                negativelong_identifiers.add(identifier)
            if is_sell_order and identifier not in negativeshort_identifiers:
                negativeshort_profits_count += 1
                negativeshort_identifiers.add(identifier)

    winratestd = positive_profits_count / (positive_profits_count + negative_profits_count) * 100 if (positive_profits_count + negative_profits_count) > 0 else 0
    winratelongstd = positivelong_profits_count / (positivelong_profits_count + negativelong_profits_count) * 100 if (positivelong_profits_count + negativelong_profits_count) > 0 else 0
    winrateshortstd = positiveshort_profits_count / (positiveshort_profits_count + negativeshort_profits_count) * 100 if (positiveshort_profits_count + negativeshort_profits_count) > 0 else 0
    
    positive_profits_count_real = sum(1 for d in data if d.get("profit", 0) > 0)

    negative_profits_count_real = sum(1 for d in data if d.get("profit", 0) < 0)
    
    winrate_value_real = positive_profits_count_real / (positive_profits_count_real + negative_profits_count_real) * 100 if (positive_profits_count_real + negative_profits_count_real) > 0 else 0
    
    unitaire_collection = db[collection_unitaire]
    unitaire_collection.update_one({}, {'$set': {'winratestdl': winratestd, 'winratereal': winrate_value_real,'winratelongstd': winratelongstd, 'winrateshortgstd': winrateshortstd }}, upsert=True)

    return winratestd, winrate_value_real, winratelongstd, winrateshortstd
