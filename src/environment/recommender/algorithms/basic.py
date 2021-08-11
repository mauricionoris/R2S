
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
import sys

sys.path.append('/source/R2S/src/util')

from cache import cached
from R2Sprofile import profileit


class PopScore():
    
    def __init__(self, parent):


        #get_class_from_frame(inspect.stack()[1][0])
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

    #recfile = '/source/R2S/cache/random.rec.pickle'
    def __init__(self, parent):
        
        self.ui_coo = parent['ui_coo']
        self.items = None
        self.rec = None


    @cached()
    def fit(self, user, n, use_cache=False):
        
        self.lil = self.ui_coo.tolil()
        rng = np.random.default_rng(1)
        rec = {}
        for i ,rated in zip(user, self.lil.rows[tuple([user])]):
            candidates = np.setdiff1d(self.items, rated, True)
            rec[i] = rng.choice(candidates, n, False)           

        return rec

    @profileit
    def recommend(self, user=None, n=10, use_cache=False):
        
        if user is None:
            user = np.unique(self.ui_coo.row)
        else:
            if len(user) == 0:
                user = np.unique(self.ui_coo.row)

        self.rec = self.fit(user, n, use_cache)

        return self.rec


    def __str__(self):
        return 'Random'


""" TODO: avoid these classes from being instantiated outside the R2S scope
import inspect

def get_class_from_frame(fr):
  args, _, _, value_dict = inspect.getargvalues(fr)
  # we check the first parameter for the frame function is
  # named 'self'
  if len(args) and args[0] == 'self':
    # in that case, 'self' will be referenced in value_dict
    instance = value_dict.get('self', None)
    if instance:
      # return its class
      caller = getattr(instance, '__class__', None)
      print(type(caller))
      if  caller != '''<class 'R2SObject.R2S'>''':
          print('here')
          raise ValueError('This class cannot be instantiated by {}'.format(caller))
          raise SystemExit
          sys.exit()

      return getattr(instance, '__class__', None)
  # return None otherwise
  return None

"""