import sys

from pymongo import MongoClient
from flask import Flask
from flask_cors import CORS

# date
from routes.date.dateDuJour import dateDuJour
from routes.date.semaineGlissante import semaineGlissante
from routes.date.semaineEnCours import semaineEnCours
from routes.date.moisEnCours import moisEnCours
from routes.date.moisGlissant import moisGlissant

# calcul
from routes.calcul.BE_RR.RR import RR
from routes.calcul.BE_RR.BE import BE
from routes.calcul.Equity import Equity
from routes.calcul.TPR import tpr
from routes.calcul.SLR import slr
from routes.calcul.Tilts import Tilts

# envoie
from routes.envoie.TPRatteint import TPRatteint
from routes.envoie.TPRnonAtteint import TPRnonAtteint

app = Flask(__name__)
CORS(app)
CORS(app, origins='*')

# date
app.register_blueprint(dateDuJour)
app.register_blueprint(semaineGlissante)
app.register_blueprint(semaineEnCours)
app.register_blueprint(moisEnCours)
app.register_blueprint(moisGlissant)

# calcul
app.register_blueprint(RR)
app.register_blueprint(BE)
app.register_blueprint(Equity)
app.register_blueprint(tpr)
app.register_blueprint(slr)
app.register_blueprint(Tilts)

# envoie
app.register_blueprint(TPRatteint)
app.register_blueprint(TPRnonAtteint)

#app.register_blueprint(Symbole)

@app.route('/')
def hello_world():
    return 'reussi en depit de ents'

if __name__ == '__main__':
    client = MongoClient("mongodb+srv://pierre:ztxiGZypi6BGDMSY@atlascluster.sbpp5xm.mongodb.net/?retryWrites=true&w=majority")
    collection = client.db["things"]
    app.run()
