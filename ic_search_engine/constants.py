'''
    Constants and weights for the aggregation pipeline.
    Modifying these weights changes what parameter is given priority when searching.
'''

#weight for pinout
PINOUT_WT = 50
#weight for pin count
PIN_COUNT_WT = 50
#weight for manufacturer name
NAME_MANUFACTURER_WT = 10
#weight for description of IC
DESCCRIPTION_WT = 5
#weight for shape of IC
SHAPE_WT = 50

def get_aggregation_pipeline(ic):
    return [
    {
        '$search': {
            'index': 'pinout_index',
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
                            'path': ['pinout'],
                            'score': {'boost': {'value': PINOUT_WT}}
                        }
                    }, {
                        'text': {
                            'query': ic['shape'],
                            'path': ['shape'],
                            'score': {'boost': {'value': SHAPE_WT}}
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
                            'score': {'boost': {'value': DESCRIPTION_WT}}
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
            'highlights': { '$meta': 'searchHighlights' },
            'description': 1,
            'manufacturer': 1
        }
    }
    ]
