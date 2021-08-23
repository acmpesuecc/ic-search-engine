from flask import Flask, jsonify

'''
    Model of an integrated circuit. Basically, a class containing all the data that
    will go in a database entry of an IC.
'''
class integrated_circuit:
    #request_dict is a dictionary of all the parameters queried through the POST request.
    def __init__(self,request_dict):
        #Get the keys of request dictionary
        keys = request_dict.keys()

        #name --> name of the IC. If no name is provided, default is "UNKNOWN"
        #For example, atmega328p
        self.name = str(request_dict['name']) if 'name' in keys else "UNKNOWN"

        #manufacturer --> name of the manufacturer. If no name is provided, default is "UNKNOWN"
        #For example, ATMEL Corporation or Texas Instruments
        self.manufacturer = str(request_dict['manufacturer']) if 'manufacturer' in keys else "UNKNOWN"

        #shape --> shape of the IC. If no name is provided, default is "UNKNOWN"
        #The shape can be square, or rectangle, etc.
        self.shape = str(request_dict['shape']) if 'shape' in keys else "UNKNOWN"

        #pin_count --> Number of pins on the IC
        #This is a number, but stored as a string
        self.pin_count = str(request_dict['pin_count']) if 'pin_count' in keys else "0"

        #description --> A brief description of the IC
        #Example: atmega328p is found in Arduinos
        self.description = str(request_dict['description']) if 'description' in keys else "UNKNOWN"

        #datasheet_link --> Link to the datasheet
        self.datasheet_link = str(request_dict['datasheet_link']) if 'datasheet_link' in keys else "UNKNOWN"

        #pinout --> A string containing a list of dictionaries that tell what pin does what.
        #example: '[{1:VCC},{2:GND}]'
        self.pinout = list()
        if 'pinout' in keys:
            self.pinout = list({str(i+1):request_dict['pinout'][str(i+1)]} if str(i+1) in request_dict['pinout'].keys() else {str(i+1):"UNKNOWN"} for i in range(int(self.pin_count)))
        self.pinout_str = str(self.pinout)

    def get_data(self,format='dict'):
        '''
            Function to get data in a usable format. This could be a JSON objet or a dictionary.
            By default, the function returns data as a dictionary, but by changing the
            'format' argument, data can be returned as a JSON object.
        '''
        #Create a dictionary with the IC's characteristics
        dict = {"name":self.name,"shape":self.shape,"manufacturer":self.manufacturer,"pin_count":self.pin_count,"description":self.description,"pinout":self.pinout, "datasheet_link": self.datasheet_link}

        #If the 'format' argument is 'dict', return data as a dictionary
        if format == 'dict':
            return dict

        #Else return data in JSON format
        return jsonify(dict)

    def get_search_data(self):
        '''
            This function returns a dictionary same as the get_data function, except the pinout_str is different. Here, the pinout_str drops any pins that are 'UNKNOWN'.
            For example: '[{1:VCC},{2:UNKNOWN},{3:GND}]' becomes '[{1:VCC},{3:GND}]'
            Also, any other unknown elements are dropped.
        '''
        #Filtering the pinout to remove any unknown pins
        filtered_pinout = filtered_pinout = list(i for i in self.pinout if list(i.items())[0][-1] != "UNKNOWN")
        #print(filtered_pinout)

        #Creating a dictionary where pinout contains filtered pinout
        dict = {"name":self.name,"shape":self.shape,"manufacturer":self.manufacturer,"pin_count":self.pin_count,"description":self.description,"pinout":filtered_pinout,"pinout_str":str(filtered_pinout)}

        #From the newly created dict, drop any items that are 'UNKNOWN'
        filtered_dict = {key: value for key, value in dict.items() if value != 'UNKNOWN'}

        #Return a dictionary with only the known items
        return dict
