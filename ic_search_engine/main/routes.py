from flask import Blueprint, render_template, redirect, url_for, request, jsonify
from ic_search_engine.extensions import mongo
from .models import integrated_circuit
from ic_search_engine.constants import *

main = Blueprint('main',__name__)

@main.route('/', methods=['GET'])
def index():
    return render_template('index.html')

@main.route('/query',methods=['POST'])
def query_data():
    ic_collection = mongo.db.ic_data
    ic = integrated_circuit(request.json).get_search_data()
    print("FOUND")
    '''<<<<<<!!! { HORRIBLY UNSAFE } !!!>>>>>>'''
    return jsonify(list(ic_collection.aggregate([
    {
        '$search': {
            'index': 'default',
            'highlight': {'path': 'pinout_str'},
            'compound': {
                'should': [
                    {
                        'text': {
                            'query': ic['pin_count'],
                            'path': ['pin_count'],
                            'score': {'boost': {'value': PIN_COUNT_WT}}
                        }
                    }, {
                        'text': {
                            'query': ic['pinout_str'],
                            'path': ['pinout_str'],
                            'score': {'boost': {'value': PINOUT_STR_WT}}
                        }
                    }, {
                        'text': {
                            'query': [ic['name'],ic['manufacturer']],
                            'path': ['manufacturer', 'name'],
                            'score': {'boost': {'value': NAME_MANUFACTURER_WT}}
                        }
                    }, {
                        'text': {
                            'query': ic['description'],
                            'path': ['description'],
                            'score': {'boost': {'value': DESCCRIPTION_WT}}
                        }
                    }
                ]
            }
        }
    }, {
        '$project': {
            'name': 1,
            'pinout': 1,
            '_id': 0,
            'score': {
                '$meta': 'searchScore'
            },
            #'highlights': { '$meta': 'searchHighlights' },
            'description': 1,
            'manufacturer': 1
        }
    }
])))

@main.route('/add',methods=['POST'])
def add_data():
    ic_collection = mongo.db.ic_data
    ic = integrated_circuit(request.json)
    ic_collection.insert_one(ic.get_data('dict'))
    return ic.get_data('json')
    #return redirect(url_for('main.index'))
