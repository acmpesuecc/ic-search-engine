'''
    Holder Class for pins data.
    This class assists the OCR script
'''

class POS:
    #Position of text in the image
    def __init__(self,x,y):
        self.x = x
        self.y = y

class pin_data_container:
    #Contains data of a pin (Data returned by the OCR)
    def __init__(self,text,pos,height,width,score):
        #Text found
        self.text = text
        #Position of text found
        self.pos = POS(pos[0],pos[1])
        #height of text found (for bounding boxes)
        self.height = height
        #height of text found (for bounding boxes)
        self.width = width
        #Score (How sure the OCR is that it is a match)
        self.score = score

    def find_dist(self,other_pin):
        #Finding min distance between two blocks of text found.
        #Two texts with minimum distance between them are usually Pairs.
        from math import sqrt
        return sqrt(pow((self.pos.x-other_pin.pos.x),2)+pow((self.pos.y-other_pin.pos.y),2))
