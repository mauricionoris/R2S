
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

from datetime import datetime

sys.path.append('/source/R2S/src/util')

from cache import cached
from R2Sprofile import profileit




class PopScore():
    
    def __init__(self, parent):

        algodata = parent.algodata[repr(self)]
        self.ui_coo = parent.ui_coo
        self.scores = parent.__dict__['data'][algodata['scores']['dataset']][algodata['scores']['feature']].value_counts() 

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

    @cached()
    def fit(self, users, n, score_method):

        items = None
        rec = {}
        if score_method == 'quantile':
            items = self.fit_by_quantile()
        if score_method == 'rank':
            items = self.fit_by_rank()
        if score_method == 'count':
            items = self.fit_by_count()

        poplist = items.sort_values(ascending=False).index[:n].to_numpy()
        for u in users:
            rec[str(u)] = poplist
        return rec



        
    #@profileit
    def recommend(self, parameters):

        self._setrecommendationparameters(parameters)

        if self.users is None:
            self.users = np.unique(self.ui_coo.row)
        else:
            if len(self.users) == 0:
                self.users = np.unique(self.ui_coo.row)

        self.rec = self.fit(self.users, self.n, self.score_method)
        return self.rec

    
    def __str__(self):
        return 'PopScore - A popularity algorithm'

    def __repr__(self):
        return 'PopScore'


    #TODO: MAKE IT GENERIC FOR ALL MODULES
    def _setrecommendationparameters(self, parameters):

        self._VALID_KEYWORDS = {'users', 'n', 'score_method'}
        for keyword, value in parameters._get_kwargs():
            if keyword in self._VALID_KEYWORDS:
                setattr(self, keyword, value)
            




class Random():

    def __init__(self, parent):
        

        algodata = parent.algodata[repr(self)]
        self.ui_coo = parent.ui_coo
        self.items = parent.__dict__['data'][algodata['items']['dataset']][algodata['items']['feature']].to_numpy()
        self.rec = None
        

    @cached()
    def fit(self, users, n):
        
        self.lil = self.ui_coo.tolil()
        rng = np.random.default_rng(1)
        rec = {}
        for i ,rated in zip(users, self.lil.rows[tuple([users])]):
            candidates = np.setdiff1d(self.items, rated, True)
            rec[str(i)] = rng.choice(candidates, n, False)   

        return rec

    #@profileit
    def recommend(self, parameters):

        self._setrecommendationparameters(parameters)


        if self.users is None:
            self.users = np.unique(self.ui_coo.row)
        else:
            if len(self.users) == 0:
                self.users = np.unique(self.ui_coo.row)

        self.rec = self.fit(self.users, self.n)

        return self.rec

    #TODO: MAKE IT GENERIC FOR ALL MODULES
    def _setrecommendationparameters(self, parameters):

        self._VALID_KEYWORDS = {'users', 'n'}
        for keyword, value in parameters._get_kwargs():
            if keyword in self._VALID_KEYWORDS:
                setattr(self, keyword, value)
            

    def __str__(self):
        return 'Random - A random algorithm'

    def __repr__(self):
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