from flask import Flask, Blueprint, jsonify, request
from pymongo import MongoClient
import bcrypt
import sys
from datetime import time
from routes.calcul.TPR import calculate_tpr
from routes.calcul.SLR import calculate_slr
from routes.calcul.killzone import calculate_killzone
from routes.calcul.session import determine_session
from routes.calcul.calculate_duration import calculate_time_duration
from routes.calcul.RR import calculate_rr
from routes.calcul.RRT import calculate_rrt
from routes.calcul.Equity import calculate_equity
from routes.calcul.weekday import add_weekday
from routes.calcul.BE import find_BE
from routes.calcul.limit import find_limit


#code groupé

from routes.calcul.max_successive_counts import find_max_successive_counts # code groupé max successive gain et max successive loss
from routes.calcul.maxprofit_minloss import find_max_profit_and_min_loss # code groupé max profit max loss
from routes.calcul.profit.profitfactorgroup import calculate_profit_factor_group
from routes.calcul.winrategroup import calculate_winrate_group
from routes.calcul.average.averagegainloss import calculate_average_gain_loss_rr
from routes.calcul.winrrtflat import calculate_winrrtflat
from routes.calcul.totaltrade import calculate_totaltrade
#from routes.calcul.average.averagetrade import calculate_averagetrade
from routes.calcul.tradecount import calculate_tradecount
from routes.calcul.tradecount import check_multiple_trades
from routes.calcul.sortiemanu import calculate_sortiemanu # penser à modifier pour appeler calculate_tpr et slr
from routes.calcul.average.daytotal import calculate_daycount
from routes.calcul.average.daytotal import calculate_averagedaytrade
from routes.calcul.average.mainasset import most_common_asset
from routes.calcul.riskcapital import calculate_risk
from routes.calcul.riskcapital import calculate_percent
from routes.calcul.overrisk import find_overrisk
from routes.calcul.overtrade import find_overtrade
from routes.calcul.profit.pfreal import calculate_pfreal

from routes.calcul.average.balanceopen import save_balance
from routes.calcul.tilt import find_tilt



#from routes.calcul.profit.profitfactor  import calculate_profit_factor // remplacé par le code groupé profit_factor_group
#from routes.calcul.profit.profitfactorlong  import calculate_profit_factor_long  // remplacé par le code groupé profit_factor_group
#from routes.calcul.profit.profitfactorshort  import calculate_profit_factor_short  // remplacé par le code groupé profit_factor_group
#from routes.calcul.minloss  import find_min_loss // remplacé par le code groupé maxprofit_minloss
#from routes.calcul.maxprofit  import find_max_profit // remplacé par le code groupé maxprofit_minloss
#from routes.calcul.max_successive_gain import find_max_successive_gains // remplacé par code groupé max_successive_count
#from routes.calcul.max_successive_losses import find_max_successive_losses // remplacé par code groupé max_successive_count
#from routes.calcul.winrate import calculate_winrate // remplacé par le code winrategroup
#from routes.calcul.winratestd  import calculate_winratestd // remplacé par le code winrategroup
#from routes.calcul.average.averagegain import calculate_average_gain // remplace par averagegainloss
#from routes.calcul.average.averageloss import calculate_average_loss // remplace par averagegainloss
#from routes.calcul.average.average_rr import calculate_average_rr // remplace par averagegainloss
#from routes.calcul.average.average_duration import calculate_average_duration // remplace par le code averagegainloss
#from routes.calcul.ddmax import calculate_ddmax // remplacé par le code maxprofit_minloss
#from routes.calcul.sharp import calculate_sharp_ratio // groupé avec maxgain_minloss

# Connexion à la base de données MongoDB
client = MongoClient("mongodb+srv://pierre:ztxiGZypi6BGDMSY@atlascluster.sbpp5xm.mongodb.net/test?retryWrites=true&w=majority")
db = client["test"]


app = Flask(__name__)
#class ModifySlException(Exception):
    #pass

# Trade Blueprint
trade_blueprint = Blueprint('trade', __name__)
SLOpen = {}
RROpen = {}
TPOpen = {}
def compare_passwords(password, hashed_password):
    return bcrypt.checkpw(password.encode('utf-8'), hashed_password)

@trade_blueprint.route('/savetraderequest', methods=['POST'])
def save_trade_request():
    data = request.json
    username = data.get('username')
    password = data.get('password')
    closure_position = data.get('closurePosition')

    client_ip = request.remote_addr
    data['client_ip'] = client_ip
 
    try:
        user = db.users.find_one({"username": username})
        if not user or not compare_passwords(password, user['password']):
            return jsonify({"message": "Access denied"}), 401

        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

        collection_name = f"{username}_open" if closure_position == "Open" else f"{username}_close"

        user_collection = db[collection_name]

        if data.get('typeOfTransaction') == "ModifySl":
            # Mettre à jour UNIQUEMENT la variable stopLoss dans la collection des ordres "Open"
            open_orders = db[f"{username}_open"]
            open_orders.update_one({"identifier": data.get('identifier')}, {"$set": {"stopLoss": data.get('stopLoss')}})
   
            rrt = calculate_rrt(data)
            data['RRT'] = rrt
            open_orders.update_one({"identifier": data.get('identifier')}, {"$set": {"RRT": data.get('RRT')}})
          
    
   

        if closure_position == "" and data.get('typeOfTransaction') == "ModifyTp":
            # Mettre à jour UNIQUEMENT la variable stopLoss dans la collection des ordres "Open"
            open_orders = db[f"{username}_open"]
            open_orders.update_one({"identifier": data.get('identifier')}, {"$set": {"stopLoss": data.get('stopLoss')}})
            open_orders.update_one({"identifier": data.get('identifier')}, {"$set": {"takeProfit": data.get('takeProfit')}})
            rrt = calculate_rrt(data)
            data['RRT'] = rrt
            open_orders.update_one({"identifier": data.get('identifier')}, {"$set": {"RRT": data.get('RRT')}})
      
            
        
        if closure_position == "Open" and data.get('typeOfTransaction') != "ModifySl":
            volume_remain = data.get('volume')
            if volume_remain < 0.01:
                volume_remain = 0
                user_collection.delete_one({"identifier": data.get('identifier')})
            identifier = data.get('identifier')
            SLOpen[identifier] = data.get('stopLoss')
            TPOpen[identifier] = data.get('takeProfit')
            if identifier not in RROpen:
                RROpen[identifier] = data.get('RRT')
            
        elif closure_position != "":
            # Check if there's a corresponding 'Open' order with the same identifier
            open_orders = db[f"{username}_open"]
            open_order = open_orders.find_one({"identifier": data.get('identifier')})
            if open_order:
                volume_remain = open_order.get('volume_remain', 0) - data.get('volume')
                if volume_remain < 0:
                    volume_remain = 0
                open_orders.update_one({"identifier": data.get('identifier')}, {"$set": {"volume_remain": volume_remain}})
                if volume_remain == 0:
                    open_orders.delete_one({"identifier": data.get('identifier')})
            else:
                return jsonify({"message": "No corresponding 'Open' order found"}), 400
        
        
        if closure_position == "ModiySl":
            data['volume'] = round(data.get('volume'), 2)
            volume_remain = round(volume_remain, 2)
            

        # Remove 'volume_remain' field for 'Close' orders
        if closure_position == "Close":
            data.pop("volume_remain", None)

            # Calculate SLR only for 'Close' orders
            slr_value = calculate_slr(data)
            data['SLR'] = slr_value['SLR']
            

            # Calculate TPR only for 'Close' orders
            tpr_value = calculate_tpr(data)
            data['TPR'] = tpr_value['TPR']
            
            
            killzone = calculate_killzone(data)
            data['killzone'] = killzone
            
            session = determine_session(data)
            data['session'] = session
            
            duration = calculate_time_duration(data)
            data['duration'] = duration['duration']
            
            rr = calculate_rr(data)
            data['RR'] = rr
            
            rrt = calculate_rrt(data)
            data['RRT'] = rrt
            
            equity = calculate_equity(data)
            data['Equity'] = equity
            
            weekday_str = add_weekday(data)
            data['Day'] = weekday_str
            
            resultBE = find_BE(data)  
            data['BE'] = resultBE

            condi = find_limit(data)
            data['Limit'] = condi

            total_trade = calculate_totaltrade(data)
            data['totaltrade'] = total_trade

            smanu = calculate_sortiemanu(data)
            data['sortiemanu'] = smanu

            new_trade_number = calculate_tradecount(data)
            data['tradecount'] = new_trade_number

            multiple = check_multiple_trades(data)
            data['simultane'] = multiple

            capitalrisk = calculate_risk(data)
            data['risk']= capitalrisk

            risk_percent = calculate_percent(data)
            data['percent']=  risk_percent

            overrisk = find_overrisk(data)
            data['overrisk'] = overrisk

            tilt_status= find_tilt(data)
            data['tilt'] = tilt_status

            overtradenumber = find_overtrade(data)
            data['overtrading'] = overtradenumber

          

            


           

       
                       

          

        # Round 'volume' and 'volume_remain' to two decimal places
        #data['volume'] = round(data.get('volume'), 2)
        #volume_remain = round(volume_remain, 2)

        # Calculate killzone only for 'Open' orders
        if closure_position == "Open":
            killzone = calculate_killzone(data)
            data['killzone'] = killzone

            session = determine_session(data)
            data['session'] = session

            rrt = calculate_rrt(data)
            data['RRT'] = rrt

            weekday_str = add_weekday(data)
            data['Day'] = weekday_str
            
            RROpen[data.get('identifier')] = rrt
             
            condi = find_limit(data)
            data['Limit'] = condi

            new_trade_number = calculate_tradecount(data)
            data['tradecount'] = new_trade_number

            multiple = check_multiple_trades(data)
            data['simultane'] = multiple

            capitalrisk = calculate_risk(data)
            data['risk']= capitalrisk

            risk_percent = calculate_percent(data)
            data['percent']=  risk_percent

            overrisk = find_overrisk(data)
            data['overrisk'] = overrisk

            #tilt_status= find_tilt(data)
            #data['tilt'] = tilt_status

            overtradenumber = find_overtrade(data)
            data['overtrading'] = overtradenumber

            
            
        # Insert the data into the collection
        #user_collection.insert_one(data)

        trade_request = {
            "username": username,
            "password": hashed_password,
            "ip" : data.get('client_ip'),
            "ticketNumber": data.get('ticketNumber'),
            "identifier": data.get('identifier'),
            "magicNumber": data.get('magicNumber'),
            "dateAndTimeOpening": data.get('dateAndTimeOpening'),
            "typeOfTransaction": data.get('typeOfTransaction'),
            "orderType": data.get('orderType'),
            "point": data.get('point'),
            "tick": data.get('tick'),
            "volume": data.get('volume'),
            "volume_remain": volume_remain,
            "symbol": data.get('symbole'),
            "priceOpening": data.get('priceOpening'),
            "stopLoss": data.get('stopLoss'),
            "SLOpen" : SLOpen.get(data.get('identifier')),
            "takeProfit": data.get('takeProfit'),
            "TPOpen" : TPOpen.get(data.get('identifier')),
            "Capitalrisk" : data.get('risk'),
            "Percent" : data.get('percent'),
            "dateAndTimeClosure": data.get('dateAndTimeClosure'),
            "priceClosure": data.get('priceClosure'),
            "swap": data.get('swap'),
            "profit": data.get('profit'),
            "Maxprofit": data.get('maxProfit'),
            "Maxloss" : data.get('maxLoss'),
            "Highestprice": data.get('highestPrice'),
            "Lowestprice": data.get('lowestPrice'),
            "commision": data.get('commision'),
            "closurePosition": data.get('closurePosition'),
            "tradecount" : data.get('tradecount'),
            "Multi" :data.get('simultane'),
            "balance": data.get('balance'),
            "broker": data.get('broker'),
            "annonceEconomique": None,
            "psychologie": None,
            "strategie": None,   
            "limit":data.get('Limit'),
            "violeStrategie": None,
            "sortie": None,
            "killzone": data.get("killzone"),
            "session": data.get("session"),
            "duration": data.get('duration'),
            "TPR": data.get('TPR'),
            "SLR": data.get('SLR'),
            "exitReason":data.get('exitReason'),
            "RR": data.get('RR'),
            "RROpen": RROpen.get(data.get('identifier')),
            "RRT": data.get('RRT'),
            "Equity": data.get('Equity'),
            "BE":data.get('BE'),
            "Day": data.get('Day'),           
            "strategie": None,
            "timeEntree": None,
            "timeSetup": None,
            "sortieManuelle":data.get('sortiemanu'),
            "tilt": data.get('tilt'),
            "TJS": None,
            "totaltrade": data.get('total_trade'),
            #"daytrade": data.get('daytrade_value'),
            "position": None,
            "typeOrdre": None,
            "indicateur1": None,
            "indicateur2": None,
            "indicateur3": None,
            "tag": [],
            "note": None,
            "overrisk" : data.get('overrisk'),
            "overtrading": data.get('overtrading')
        }
        if not (data.get('closure_position') == "" and data.get('typeOfTransaction') == "ModifySl"):
            data["volume_remain"] = volume_remain
    
        #combined_data = [trade_request, data]
        # Insertion des données dans la collection
            
        user_collection.insert_one(trade_request)
      
     
        find_max_successive_counts(data)
        find_max_profit_and_min_loss(data)
        calculate_profit_factor_group(data)
        calculate_winrate_group(data)
        calculate_average_gain_loss_rr(data) 
        calculate_winrrtflat(data)
        calculate_totaltrade(data)
        calculate_daycount(data)
        calculate_averagedaytrade(data)
        most_common_asset(data)
        save_balance(data)
        calculate_pfreal(data)

        #calculate_profitw(data)
   
        
             
        #calculate_profit_factor(data)  // remplacé par le code groupé profit_factor_group        
        #calculate_profit_factor_long(data)   // remplacé par le code groupé profit_factor_group            
        #calculate_profit_factor_short(data)  // remplacé par le code groupé profit_factor_group           
        #find_min_loss(data)   // remplacé par le code groupé maxprofit_minloss            
        #find_max_profit(data)  // remplacé par le code groupé maxprofit_minloss
        #find_max_successive_gains(data) // remplacé par code groupé max_successive_count          
        #find_max_successive_losses(data) // remplacé par code groupé max_successive_count
        #calculate_winrate(data) // remplacé par le code winrategroup           
        #calculate_winratestd(data) // remplacé par le code winrategroup
        #calculate_average_gain(data)  // remplace par averagegainloss
        #calculate_average_loss(data) // remplace par averagegainloss 
        #calculate_average_rr(data) // remplace par averagegainloss
        #calculate_average_duration(data) // remplace par le code averagegainloss
        #calculate_ddmax(data)  // remplacé par le code maxprofit_minloss
        #calculate_sharp_ratio(data) // groupé avec maxgain_minloss
        
        return jsonify({"message": "Data saved successfully with TPR and SLR kill"}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 400

# Enregistrement du blueprint "trade" dans l'application Flask
app.register_blueprint(trade_blueprint, url_prefix='/api')


if __name__ == '__main__':
    app.run()
