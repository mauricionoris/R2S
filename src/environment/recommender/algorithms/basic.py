
# extracted and adapted from Lenskit for R2S purposes
""" 
    basic.py
    

"""

#AlgoParam = Enum('score_method', 'quantile rank count')


import pandas as pd
import numpy as np
import scipy.sparse as spa
import pickle
import os.path


class PopScore():
    
    def __init__(self, parent):

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


    def __init__(self, parent):
        

        
        recfile = '/source/R2S/cache/random.rec.pickle'
        #candidatesfile = '/source/R2S/cache/user.candidates.pickle'
        cached_data = {}
        candidates = {}

        if os.path.isfile(recfile) == True:
            try:
                # Load data (deserialize)
                with open(recfile, 'rb') as handle:
                    cached_data = pickle.load(handle)
            except:
                cached_data = {}

        #if os.path.isfile(candidatesfile) == True:
        #    # Load data (deserialize)
        #    with open(candidatesfile, 'rb') as handle:
        #        candidates = pickle.load(handle)


        self.ui_coo = parent['ui_coo']
        self.items = None
        self.rec = cached_data
        #self.candidates = candidates

    #EVALUATE CANDIDATES CACHE GENERATION
    #def getcandidates(self, user):

    #    missingusers = np.setdiff1d(user, list(self.candidates.keys()), True)
    #    for i ,rated in zip(user, self.lil.rows[tuple([missingusers])]):
    #        self.candidates[i] = np.setdiff1d(self.items, rated, True)
        
    #    return True

    
    def fit(self, user, n):
        
        self.lil = self.ui_coo.tolil()
        rng = np.random.default_rng(1)

        #self.getcandidates(user)
        for i ,rated in zip(user, self.lil.rows[tuple([user])]):
            #print('generating new recommendations for user: {} '.format(i))
            #self.rec[i] = rng.choice(self.candidates[i], n, True).tolist()
            candidates = np.setdiff1d(self.items, rated, True)
            self.rec[i] = rng.choice(candidates, min(len(candidates),n), False)           



    def recommend(self, user=None, n=10, clean_cache=False):
        
        if user is None:
            user = np.unique(self.ui_coo.row)
        else:
            if len(user) == 0:
                user = np.unique(self.ui_coo.row)


        if clean_cache == True:
            print('Cleaning {} users cached'.format(len(self.rec.keys())))
            self.rec = {}
        else:
            user = np.setdiff1d(user, list(self.rec.keys()), True)
            print('Users from cache {}'.format(len(self.rec.keys())))



        print('New users {}'.format(len(user)))


        self.fit(user, n)
        


        return self.rec












    def __str__(self):
        return 'Random'


