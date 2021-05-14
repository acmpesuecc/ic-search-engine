from flask import Flask, jsonify

class integrated_circuit:
    def __init__(self,request_dict):
        keys = request_dict.keys()
        self.name = str(request_dict['name']) if 'name' in keys else "UNKNOWN"
        self.manufacturer = str(request_dict['manufacturer']) if 'manufacturer' in keys else "UNKNOWN"
        self.pin_count = str(request_dict['pin_count']) if 'pin_count' in keys else "UNKNOWN"
        self.description = str(request_dict['description']) if 'description' in keys else "UNKNOWN"
        self.pinout = dict()
        if 'pinout' in keys:
            for i in range(int(self.pin_count)):
                self.pinout[str(i+1)] = "UNKNOWN"
                if str(i+1) in request_dict['pinout'].keys():
                    self.pinout[str(i+1)] = request_dict['pinout'][str(i+1)]
        self.pinout_str = str(self.pinout)

    def get_data(self,format='dict'):
        dict = {"name":self.name,"manufacturer":self.manufacturer,"pin_count":self.pin_count,"description":self.description,"pinout":self.pinout,"pinout_str":self.pinout_str}
        if format == 'dict':
            return dict
        return jsonify(dict)

    def get_search_data(self):
        filtered_pinout = {key: value for key, value in self.pinout.items() if value != 'UNKNOWN'}
        dict = {"name":self.name,"manufacturer":self.manufacturer,"pin_count":self.pin_count,"description":self.description,"pinout":filtered_pinout,"pinout_str":str(filtered_pinout)}
        filtered_dict = {key: value for key, value in dict.items() if value != 'UNKNOWN'}
        return dict
