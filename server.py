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
from routes.calcul.profit.profitfactor import profitfactor
from routes.calcul.profit.profitfactorlong import profitfactorlong
from routes.calcul.profit.profitfactorshort import profitfactorshort
from routes.calcul.average.averagegain import averagegain
from routes.calcul.average.averageloss import averageloss
from routes.calcul.average.average_duration import average_duration
from routes.calcul.winrate import winrate
from routes.calcul.maxprofit import maxprofit
from routes.calcul.minloss import minloss
from routes.calcul.calculate_duration import calculate_duration
from routes.calcul.ddmax import ddmax
from routes.calcul.killzone import killzone
from routes.calcul.session import session
from routes.calcul.sharp import sharp_ratio
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
app.register_blueprint(profitfactor)
app.register_blueprint(profitfactorlong)
app.register_blueprint(profitfactorshort)
app.register_blueprint(winrate)
app.register_blueprint(averagegain)
app.register_blueprint(averageloss)
app.register_blueprint(average_duration)
app.register_blueprint(maxprofit)
app.register_blueprint(minloss)
app.register_blueprint(calculate_duration)
app.register_blueprint(ddmax)
app.register_blueprint(session)
app.register_blueprint(sharp_ratio)
app.register_blueprint(killzone)




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
