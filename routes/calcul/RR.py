from pymongo import MongoClient

# Connexion à la base de données MongoDB
client = MongoClient('mongodb+srv://pierre:ztxiGZypi6BGDMSY@atlascluster.sbpp5xm.mongodb.net/?retryWrites=true&w=majority')
db = client['test']

def calculate_rr(data):
    # Calculer la valeur de la clé "RR" pour chaque élément en une seule étape
    price_close = data['priceClosure']
    price_opening = data['priceOpening']
    stop_loss = data['stopLoss']
    rr_values = [(pc - po) + (po - sl) for pc, po, sl in zip(price_close, price_opening, stop_loss)]

    return rr_values  # Renvoie les valeurs de la clé "RR" en tant que liste JSON

