from flask import Flask, Blueprint, jsonify
from pymongo import MongoClient
from datetime import datetime

assign_order = Blueprint('assign_order', __name__)

client = MongoClient('mongodb+srv://pierre:ztxiGZypi6BGDMSY@atlascluster.sbpp5xm.mongodb.net/test?retryWrites=true&w=majority')
db = client['test']
collection_things = db['things']

@assign_order.route('/assign_order', methods=['GET'])
def assign_order_fn():
    sorted_documents = collection_things.find().sort("dateAndTimeOpening", 1)
    
    order_dict = {}
    
    for document in sorted_documents:
        current_date = document["dateAndTimeOpening"].date()
        ticket_number = document["ticketNumber"]
        
        if current_date not in order_dict:
            order_dict[current_date] = {}
        
        if ticket_number in order_dict[current_date]:
            order = order_dict[current_date][ticket_number]
        else:
            order = len(order_dict[current_date]) + 1
            order_dict[current_date][ticket_number] = order
        
        collection_things.update_one({"_id": document["_id"]}, {"$set": {"order": order}})
    
    return "Order assignment completed."