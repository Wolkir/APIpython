import sys

from pymongo import MongoClient
from flask import Flask
from flask_cors import CORS

# user
from connexion.user.login import setup_login_routes
from connexion.user.signup import setup_signup_route

#from connexion.tradReq import trade_blueprint
from connexion.tradReq.tradReq import trade_blueprint

from connexion.strategie.createStrategie import createStrategie
from connexion.strategie.suppressionStrategie import suppressionStrategie
from connexion.strategie.recuperationStrategie import recuperationStrategie

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
from routes.calcul.weekday import weekday
from routes.calcul.tradecount import tradecount
from routes.calcul.assign_order import assign_order
from routes.calcul.average.average_rr import average_rr
from routes.calcul.conversion_map import conversion_map

# envoie
from routes.envoie.envoie import envoie

app = Flask(__name__)
CORS(app)
CORS(app, origins='*')

# user
app.register_blueprint(setup_signup_route(app))
app.register_blueprint(setup_login_routes(app))
app.register_blueprint(trade_blueprint)
"""
app.register_blueprint(login)
app.register_blueprint(signup)
app.register_blueprint(createStrategie)
app.register_blueprint(suppressionStrategie)
app.register_blueprint(recuperationStrategie)
app.register_blueprint(trade_blueprint)

app.register_blueprint(strategie_blueprint)

# date
app.register_blueprint(dateDuJour)
app.register_blueprint(semaineGlissante)
app.register_blueprint(semaineEnCours)
app.register_blueprint(moisEnCours)
app.register_blueprint(moisGlissant)
app.register_blueprint(Symbole)
"""
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
app.register_blueprint(weekday)
app.register_blueprint(tradecount)
app.register_blueprint(assign_order)
app.register_blueprint(average_rr)
# app.register_blueprint(conversion_map)

# envoie
app.register_blueprint(envoie)

#app.register_blueprint(Symbole)

@app.route('/')
def hello_world():
    return 'reussi en depit de ents'

if __name__ == '__main__':
    url = "mongodb+srv://pierre:ztxiGZypi6BGDMSY@atlascluster.sbpp5xm.mongodb.net/?retryWrites=true&w=majority"
    client = MongoClient(url, connectTimeoutMS=30000, socketTimeoutMS=None, connect=False, maxPoolsize=1)
    collection = client.db["things"]
    app.run(host='0.0.0.0', port=1234)
    app.run(host='0.0.0.0', port=1234)
