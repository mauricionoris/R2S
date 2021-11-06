import sys

sys.path.append('/source/R2S/src/util')
sys.path.append('/source/R2S/src/environment/recommender')


#from R2Sprofile import profileit
import R2SObject
#import pandas as pd
import numpy as np
import argparse 
from argparse import Namespace


parser=argparse.ArgumentParser()

import time                                                



#@profileit
def callR2S(env, action, parameters):

    #print('Environment:', env)
    #print('Action:', action)
    #print('parameters:', parameters)
    

    #Setting the Environment
    R2SEnv = R2SObject.R2S(env)

    #Executing an action
    ts = time.time()
    ret = R2SEnv.algo[action.algo].recommend(parameters)
    te = time.time()

    for i in parameters.users:
        print('User {} --> Recommendations {}'.format(i,ret[str(i)]))

    print ('Time elapsed {} to run {} algorithm '.format(te-ts, action.algo) )
    
    """"
    print(ret['metadata'])

    #JUST FOR TESTING PURPOSES. It will execute an algorithm setted at the action parameter
    print('available algorithms')

    for available_algorithm in R2SEnv.algo:
        ts = time.time()
        ret = R2SEnv.algo[available_algorithm].recommend(parameters)
        te = time.time()
       for i in parameters.users:
            print('User {} --> Recommendations {}'.format(i,ret[str(i)]))
        print ('Time elapsed {} to run {} algorithm '.format(te-ts, available_algorithm) )
        print(ret['metadata'])
    """
    return ret['metadata']


if __name__ == '__main__':

    env = argparse.Namespace(dataset={'name':'MovieLens', 'path':'/source/R2S/data/R2SDatasets/movielens'}
#                   , data={'ratings':None, 'movies': None, 'tags': None, 'links': None, 'genome-tags':None, 'genome-scores': None}
                    , data={'ratings':None, 'movies': None} #TODO: specify the columns to load to avoid loading the whole file
                    , matrix={'source':'ratings', 'row':'userId', 'col':'movieId', 'data':'rating'}
                    , algo={ 'Random':'basic','PopScore': 'basic'}
#                   , algo={'PopScore': 'basic'}
#                   , algo={'Random':'basic'}
                    , algodata={'Random':{'items':{'dataset':'movies', 'feature':'movieId'}}
                               ,'PopScore':{'scores':{'dataset':'ratings','feature':'movieId'}}})

    param = argparse.Namespace(users = [25,26,27,28,29,30,31,32], n = 3, score_method = 'count')


    actions = argparse.Namespace(algo = 'Random')

    #print(args)
    print(callR2S(env, actions, param))
    sys.exit(0) #exit code of the script

