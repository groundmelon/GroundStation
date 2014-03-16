# -*- coding: utf-8 -*- 

import cPickle

class PickleFileIO(object):
    def __init__(self, filepath):
        self.filepath = filepath
    
    def save(self,data):
        f = open(self.filepath,"wb")
        cPickle.dump(data, f)
        f.close()
        
    def load(self):
        data = None
        f = open(self.filepath,"rb")
        data = cPickle.load(f)
        f.close()
        return data
