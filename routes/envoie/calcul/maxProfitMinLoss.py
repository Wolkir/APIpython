from pymongo import MongoClient
import numpy as np

client = MongoClient('mongodb+srv://pierre:ztxiGZypi6BGDMSY@atlascluster.sbpp5xm.mongodb.net/?retryWrites=true&w=majority')
db = client['test']

def maxProfitMinLoss(data, collection_unitaire):
    max_profit_value = float('-inf')
    min_loss_value = float('inf')
    max_equity = None
    all_profits = []

    for doc in data:
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

    unitaire_collection = db[collection_unitaire]
    unitaire_collection.update_one(
        {},
        {'$set': {'sharpe': sharpe_ratio, 'Max profit': max_profit_value, 'Max loss': min_loss_value, 'dd max': max_equity}},
        upsert=True
    )

    return sharpe_ratio, max_profit_value, min_loss_value, max_equity

