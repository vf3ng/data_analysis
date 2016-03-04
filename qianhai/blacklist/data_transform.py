#coding=uft-8

import pandas as pd
import json

class Data(object):

    def __init__(self,file):
        self.data = []
        json_data = open(file,r).readlines()
        for line in json_data:
            value = json.loads(line)
            self.data.append(value['records'])
         

    def get_data(self):
        data = pd.DataFrame(self.data)
        return data       
