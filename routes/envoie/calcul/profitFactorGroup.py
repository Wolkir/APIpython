from pymongo import MongoClient

client = MongoClient('mongodb+srv://pierre:ztxiGZypi6BGDMSY@atlascluster.sbpp5xm.mongodb.net/?retryWrites=true&w=majority')
db = client['test']

def profitFactorGroup(data, collection_unitaire):

    total_profit = 0
    total_loss = 0

    total_profit_buy = 0
    total_loss_buy = 0

    total_profit_sell = 0
    total_loss_sell = 0

    for doc in data:
        profit = doc['profit']
        type_of_transaction = doc['orderType']
        
        if profit > 0:
            total_profit += profit
        elif profit < 0:
            total_loss += profit

        if type_of_transaction == "BUY":
            if profit > 0:
                total_profit_buy += profit
            elif profit < 0:
                total_loss_buy += profit
        
        elif type_of_transaction == "SELL":
            if profit > 0:
                total_profit_sell += profit
            elif profit < 0:
                total_loss_sell += profit

    if total_loss != 0:
       profit_factor = total_profit / abs(total_loss)
    else:
       profit_factor = 0

    if total_loss_buy != 0:
       profit_factor_buy = total_profit_buy / abs(total_loss_buy)
    else:
       profit_factor_buy = 0

    if total_loss_sell != 0:
       profit_factor_sell = total_profit_sell / abs(total_loss_sell)
    else:
       profit_factor_sell = 0

    unitaire_collection = db[collection_unitaire]
    unitaire_collection.update_one(
        {},
        {
            '$set': {
                'profitfactor': profit_factor,
                'profitfactorlong': profit_factor_buy,
                'profitfactorshort': profit_factor_sell,
                'total gain': total_profit,
                'total loss': total_loss,
                'total gain long': total_profit_buy,
                'total loss long': total_loss_buy,
                'total gain short': total_profit_sell,
                'total loss short': total_loss_sell            
                
            }
        },
        upsert=True
    )

    return profit_factor, profit_factor_buy, profit_factor_sell, total_profit, total_loss, total_profit_buy, total_loss_buy, total_profit_sell, total_loss_sell
