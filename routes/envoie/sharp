from flask import Blueprint, jsonify
from pymongo import MongoClient
import numpy as np

client = MongoClient('mongodb+srv://pierre:ztxiGZypi6BGDMSY@atlascluster.sbpp5xm.mongodb.net/?retryWrites=true&w=majority')
db = client['test']

def sharp(data, collection_unitaire):

    profits = [doc['profit'] for doc in data]

    sharpe_ratio = np.mean(profits) / np.std(profits) if np.std(profits) > 0 else 0

    unitaire_collection = db[collection_unitaire]
    unitaire_collection.update_one({}, {"$set": {"sharpe": sharpe_ratio}}, upsert=True)

    return sharpe_ratio
