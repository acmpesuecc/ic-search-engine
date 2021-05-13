from flask import Blueprint, render_template, redirect, url_for, request
from ic_search_engine.extensions import mongo
from .models import integrated_circuit

main = Blueprint('main',__name__)

@main.route('/', methods=['GET'])
def index():
    return render_template('index.html')

@main.route('/query',methods=['POST'])
def query_data():
    ic_collection = mongo.db.ic_data
    print(request.json)
    print("FOUND")
    '''<<<<<<!!! { HORRIBLY UNSAFE } !!!>>>>>>'''
    return str(ic_collection.find_one(request.json))

@main.route('/add',methods=['POST'])
def add_data():
    ic_collection = mongo.db.ic_data
    ic = integrated_circuit(request.json)
    ic_collection.insert_one(ic.get_data('dict'))
    return ic.get_data('json')
    #return redirect(url_for('main.index'))
