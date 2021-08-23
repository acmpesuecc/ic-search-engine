'''
    OCR script. Extracts pin information from pinout diagram
'''

#imports
import easyocr
import cv2
from .holder_class import pin_data_container

class identifier:
    #identifier class
    def __init__(self,img_addr):
        #All acceptable characters
        self.acceptable = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz_0123456789'
        #read image as a numpy array using cv2's imread() func
        self.img = cv2.imread(img_addr)
        #Location of the image
        self.img_addr = img_addr
        #Height and width of the image
        self.hImg, self.wImg = self.img.shape[:2]
        #self.clean_image()
        #Empty lists for pins
        self.pins_list = list()
        self.pin_nos_list = list()

    #def clean_image(self):
    #    ret,self.img = cv2.threshold(self.img,127,255,cv2.THRESH_BINARY)

    def text_from_img(self):
        '''
            Extracts text from image, stores it in pins_list and pin_nos_list
        '''
        #initialize the OCR
        reader = easyocr.Reader(['en'],gpu=True)
        #Read text from image
        result = reader.readtext(self.img_addr)
        pins_list = list()
        pin_nos_list = list()
        for i in result:
            #For every text found, check if characters are acceptable
            text = ''.join(list(filter(lambda x: x in self.acceptable, i[-2])))
            #score is the last item in the result list
            score = i[-1]
            #Get width, height, x and y of the text found
            w = i[0][0][0] - i[0][2][0]
            h = i[0][0][1] - i[0][2][1]
            x = i[0][0][0]
            y = i[0][0][1]
            #Filter false positives
            if len(text) == 1 and score <= 0.8:
                pass
            else:
                if len(text.split(' ')) > 1 and text.split(' ')[0].isdigit():
                    if not text.split(' ')[1].isdigit() and len(text.split(' ')[1]) > 2:
                        new_pin1 = pin_data_container(text.split(' ')[0],(x,y),h,w,score)
                        new_pin2 = pin_data_container(text.split(' ')[1],(x,y),h,w,score)
                        pins_list.append(new_pin2)
                        pin_nos_list.append(new_pin1)
                else:
                    new_pin = pin_data_container(text,(x,y),h,w,score)
                    if text.isdigit():
                        pin_nos_list.append(new_pin)
                    else:
                        pins_list.append(new_pin)
        self.pins_list = pins_list
        self.pin_nos_list = pin_nos_list
        return pins_list, pin_nos_list

    def get_pins_dict(self):
        #First get text from image
        self.text_from_img()
        max_w = abs(max(list(x.width for x in self.pins_list)))
        pins_dict = {}
        #Then convert it to a dict.
        for i in self.pin_nos_list:
            dists = [x.find_dist(i) for x in self.pins_list]
            min_ = min(dists)
            min_index = dists.index(min(dists))
            if min_ <= max_w + self.hImg//8:
                pins_dict[i.text] = self.pins_list[min_index]
                self.pins_list.pop(min_index)
                dists = [x.find_dist(i) for x in self.pins_list]
            if len(self.pins_list) == 0:
                    break
        #Return said dictionary
        return pins_dict

if __name__ == '__main__':
    img_path = 'pin4.jpg'
    #img = cv2.imread(img_path)
    x = identifier(img_path)
    x.text_from_img()
    d = x.get_pins_dict()

    for i in sorted(d.keys(),key=lambda x: int(x)):
        if len(d[i].text) > 0:
            print(i,':',d[i].text)
