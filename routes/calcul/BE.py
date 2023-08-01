from flask import Flask, Blueprint, jsonify
from pymongo import MongoClient

BE = Blueprint('BE', __name__)

# Connexion à la base de données MongoDB
client = MongoClient('mongodb+srv://pierre:ztxiGZypi6BGDMSY@atlascluster.sbpp5xm.mongodb.net/?retryWrites=true&w=majority')
db = client['test']


def find_BE(data):
    resultBE = {}  # Initialize the 'order' dictionary

    rr = calculate_rr(data)

    if data['closurePosition'] == "Close" and rr is not None and -0.5 < rr < 0.5:
        resultBE['BE'] = True
    else:
        resultBE['BE'] = False

    return resultBE  # Renvoie la valeur de BE
