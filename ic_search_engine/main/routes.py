'''
    This file contains all routes of the web application.
'''

#Importing required files
from flask import Blueprint, send_from_directory, redirect, url_for, request, jsonify, current_app
from werkzeug.utils import secure_filename
from ic_search_engine.extensions import mongo
from .models import integrated_circuit
from ic_search_engine.constants import *
from ic_search_engine.ocr import *
import os

main = Blueprint('main',__name__)
#main.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

#All valid extensions allowed
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg'])

#Utility func to check if file extension is valid
def allowed_file(filename):
    extension = filename.split('.')[-1]
    if extension in ALLOWED_EXTENSIONS:
        return True
    return False

'''
    The main route. Accesses the home page.
'''
@main.route('/', methods=['GET'])
def index():
    #Renders the template in index.html
    return send_from_directory(current_app.static_folder,'index.html')

'''
    Route to query for ICs.
    Queries are sent to this route in the body of a POST request as a JSON from_object.
    Possible matches are returned as a JSON object.
'''
@main.route('/query',methods=['POST'])
def query_data():
    #Create an object to access the database
    ic_collection = mongo.db.ic_data
    #Get search parameters from the request
    ic = integrated_circuit(request.json).get_search_data()
    #Use an aggregation pipeline to find best matches, and return those matches
    #in a JSON object
    return jsonify(list(ic_collection.aggregate(get_aggregation_pipeline(ic))))

'''
    Route to add new ICs to the database.
    This route takes information from the users about new ICs and adds it to the database.
'''
@main.route('/add',methods=['POST','GET'])
#TODO: Add some form of authentication to be able to access this resource.
def add_data():
    try:
        # check if the post request has the file part
        if request.method == 'POST':
            #Check if the incoming request contains a file
            print(request.files)
            for i in request.files:
                print(i)
            print(request.json)
            if 'pinout_diagram' not in request.files:
                return {'error':'Please upload the required file'}, 406
            pinout_diagram = request.files['pinout_diagram']
            #In case filename is empty (file hasn't been uploaded)
            if pinout_diagram.filename == '':
                return {'error':'Please select a pinout file'}, 406
            #Check if the uploaded pinout diagram is a valid image file
            if pinout_diagram and allowed_file(pinout_diagram.filename):
                #Randomly generated file name for security reasons
                filename = secure_filename(pinout_diagram.filename)
                #Save the file to a temporary location while we retrieve pinout from it.
                pinout_diagram.save(os.path.join(current_app.config['UPLOAD_FOLDER'], filename))
                #Get data from pinout. If error, send back error msg.
                #STEP 0: Get the path of the file just saved
                file_path = os.path.join(current_app.config['UPLOAD_FOLDER'],filename)
                #Putting steps 1 and 2 in a try and except block to handle errors.
                try:
                    #STEP 1: Create an identifier object. (The class exists in ocr.py)
                    ocr_object = identifier(file_path)
                    #STEP 2: Get pinout information
                    pinout_info = ocr_object.get_pins_dict()
                except Exception as e:
                    #delete saved image, then return error message
                    #os.system('rm '+file_path)
                    return {'error':str(e)}, 418
                    #return {'error':'There was some error while reading pinout information from the image. Try again later.'}, 418
                #If all goes well:
                ic_collection = mongo.db.ic_data
                ic = integrated_circuit(request.json)
                ic_collection.insert_one(ic.get_data('dict'))
                #delete saved image, then send success message
                #os.system('rm '+file_path)
                return ic.get_data('json')
            #If pinout image is of the wrong format
            else:
                #delete saved image, then returh error message
                #os.system('rm '+file_path)
                return {'error':'Please select a valid pinout file'}, 415
        elif request.method == 'GET':
            return send_from_directory(current_app.static_folder,'add.html')
    except:
        return {'error':'Something bad on our end, sorry!'}, 500
