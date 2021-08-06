
# extracted and adapted from Lenskit for R2S purposes
""" 
    basic.py
    

"""

#AlgoParam = Enum('score_method', 'quantile rank count')


import pandas as pd
import numpy as np
import scipy.sparse as spa


class PopScore():
    
    def __init__(self, **kwargs):

        #self.scores = ratings['item'].value_counts()
        self.scores = None 
        self.score_method = None 

    def fit_by_quantile(self):
        print('by quantile')
        cmass = self.scores.sort_values()
        cmass = cmass.cumsum()
        cdens = cmass / self.scores.sum()
        return cdens.sort_index()

    def fit_by_rank(self):
        print('by rank')
        return self.scores.rank().sort_index()

    def fit_by_count(self):
        print('by count')
        return self.scores.sort_index()

    def fit(self):

        if self.score_method == 'quantile':
            return self.fit_by_quantile()
        if self.score_method == 'rank':
            return self.fit_by_rank()
        if self.score_method == 'count':
            return self.fit_by_count()
        

class Random():


    def __init__(self):
        

        self.ui_coo = None
        self.items = None
        self.rec = {}

    def fit(self, user, n):
        
        self.lil = self.ui_coo.tolil()
        rng = np.random.default_rng(1)
        if user == None:
            print('generating recommendations for all users')
            i = 0
            for rated in self.lil.rows:
                self.rec[i] = rng.choice(np.setdiff1d(self.items, rated, True), n, True).tolist()
                i +=1

        else:
            for i ,rated in zip(user, self.lil.rows[tuple([user])]):
                print('generating recommendations for user {} '.format(i))
                self.rec[i] = rng.choice(np.setdiff1d(self.items, rated, True), n, True).tolist()
            



    def recommend(self, user=None, n=10):

        if self.rec == {}:
            self.fit(user, n)
        
        #if user != None:
        #    print(self.rec)
        #    print(user)
           # return self.rec[[user]]

        return self.rec












    def __str__(self):
        return 'Random'


